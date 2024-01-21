from odoo import fields, models, _


class ExpenseSheet(models.Model):
    _name = "hr.expense.sheet"
    _inherit = ["hr.expense.sheet", "l10n_do.gov.sign.document"]

    l10n_do_gov_signing_request_ids = fields.One2many(
        "l10n_do_gov.document.signing.request",
        "expense_sheet_id",
        "Signing/Approval Requests",
        readonly=True,
    )

    def action_cron_update_signing_request_status_expense(self):
        pending_expenses = self.search(
            [
                ("signing_request_finished", "=", False),
                ("request_public_access_id", "!=", False),
            ]
        )
        for expense in pending_expenses:
            expense.update_signing_request_status()

    def action_signing_request_wizard(self):
        self.ensure_one()

        template_id = self.env["ir.model.data"]._xmlid_lookup(
            "l10n_do_gov_sign_expense.email_template_expense_report"
        )[2]

        ctx = dict(self.env.context or {})
        ctx.update(
            {
                "active_model": "hr.expense.sheet",
                "active_id": self.ids[0],
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
            }
        )

        name = _("Expense Report Signing Request")

        return {
            "name": name,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "l10n_do.gov.sign.request.wizard",
            "target": "new",
            "context": ctx,
        }
