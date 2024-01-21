from odoo import _, fields, models


class Purchase(models.Model):
    _inherit = "purchase.order"

    l10n_do_gov_signing_request_ids = fields.One2many(
        "l10n_do_gov.document.signing.request",
        "purchase_id",
        "Signing/Approval Requests",
        readonly=True,
    )

    def action_cron_update_signing_request_status_purchase(self):
        pending_orders = self.search(
            [
                ("signing_request_finished", "=", False),
                ("request_public_access_id", "!=", False),
            ]
        )
        for po in pending_orders:
            po.update_signing_request_status()

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
