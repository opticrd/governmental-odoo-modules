from datetime import datetime as dt

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class GovSignDocument(models.Model):
    _name = "l10n_do.gov.sign.document"
    _description = "Dominican Gov Sign Document"

    request_public_access_id = fields.Char(copy=False)
    document_public_access_id = fields.Char(copy=False)
    signing_request_finished = fields.Boolean(copy=False)

    def finalize_document_signing_request(self):
        self.ensure_one()
        if not self.request_public_access_id:
            raise ValidationError(_("Missing Public Access ID for finalize request."))
        self.env["l10n_do.gov.sign"].finalize_signing_request(
            self.request_public_access_id
        )

        pending_sign_request = self.l10n_do_gov_signing_request_ids.filtered(
            lambda req: req.status in ("NEW", "READ")
        )
        pending_sign_request.write({"status": "NO_ACTION"})
        self.signing_request_finished = True

        if self.l10n_do_gov_signing_request_ids.filtered(
            lambda sq: sq.status == "SIGNED"
        ):
            self._message_post_signed_document()

    def update_signing_request_status(self):
        self.ensure_one()
        if not self.request_public_access_id:
            raise ValidationError(_("Missing Public Access ID for status request."))
        result = self.env["l10n_do.gov.sign"].get_request_data(
            self.request_public_access_id
        )
        comments_data = result.get("comments", [])

        def get_comment(userCode):
            comment = False
            for comment in comments_data:
                if comment["userCode"] == userCode:
                    comment = comment["comment"]
            return comment

        for addressee in result["addresseeLines"][0]["addresseeGroups"]:
            entity_data = addressee["userEntities"][0]
            sign_request_id = self.l10n_do_gov_signing_request_ids.filtered(
                lambda req: req.user_id.l10n_do_gov_sign_username
                == entity_data["userCode"]
            )
            if sign_request_id and entity_data["status"] != sign_request_id.status:
                action_date = (
                    dt.fromtimestamp(
                        int(entity_data["actionInfo"]["date"]) / 1000
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    if "actionInfo" in entity_data
                    else fields.Datetime.now()
                )
                sign_request_id.write(
                    {
                        "status": entity_data["status"],
                        "action_date": action_date,
                        "comment": get_comment(entity_data["userCode"]),
                    }
                )

        if not hasattr(self, "l10n_do_gov_signing_request_ids"):
            raise ValidationError(_("There is not document signing module installed."))

        pending_sign_request = self.l10n_do_gov_signing_request_ids.filtered(
            lambda req: req.status in ("NEW", "READ")
        )
        if not pending_sign_request:
            self.finalize_document_signing_request()

    def _message_post_signed_document(self):
        self.ensure_one()
        result = self.env["l10n_do.gov.sign"].get_signed_document(
            self.document_public_access_id
        )

        attachment = self.env["ir.attachment"].create(
            {
                "name": result["filename"],
                "datas": bytes(result["base64"], encoding="utf-8"),
            }
        )
        self.message_post(attachment_ids=[attachment.id])
