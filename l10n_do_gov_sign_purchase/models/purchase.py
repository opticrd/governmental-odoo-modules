from datetime import datetime as dt

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class Purchase(models.Model):
    _inherit = "purchase.order"

    request_public_access_id = fields.Char(copy=False)
    document_public_access_id = fields.Char(copy=False)
    signing_request_finished = fields.Boolean(copy=False)
    l10n_do_gov_signing_request_ids = fields.One2many(
        "l10n_do_gov.document.signing.request",
        "purchase_id",
        "Signing/Approval Requests",
        readonly=True,
    )

    def action_cron_update_signing_request_status(self):
        pending_orders = self.search(
            [
                ("signing_request_finished", "=", False),
                ("request_public_access_id", "!=", False),
            ]
        )
        for po in pending_orders:
            po.update_signing_request_status()

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

    def finalize_signing_request(self):
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

        pending_sign_request = self.l10n_do_gov_signing_request_ids.filtered(
            lambda req: req.status in ("NEW", "READ")
        )
        if not pending_sign_request:
            self.finalize_signing_request()

    def action_signing_request_wizard(self):
        self.ensure_one()

        ir_model_data = self.env["ir.model.data"]
        try:
            if self.env.context.get("send_rfq", False):
                template_id = ir_model_data._xmlid_lookup(
                    "purchase.email_template_edi_purchase"
                )[2]
            else:
                template_id = ir_model_data._xmlid_lookup(
                    "purchase.email_template_edi_purchase_done"
                )[2]
        except ValueError:
            template_id = False

        ctx = dict(self.env.context or {})
        ctx.update(
            {
                "active_model": "purchase.order",
                "active_id": self.ids[0],
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "custom_layout": "mail.mail_notification_paynow",
                "force_email": True,
                "mark_rfq_as_sent": True,
            }
        )

        if self.state in ["draft", "sent"]:
            name = _("RFQ Signing Request")
        else:
            name = _("Purchase Order Signing Request")

        return {
            "name": name,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "l10n_do.gov.sign.request.wizard",
            "target": "new",
            "context": ctx,
        }
