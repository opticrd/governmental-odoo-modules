from odoo import models, fields


class SignRequest(models.Model):
    _inherit = "l10n_do_gov.document.signing.request"

    expense_sheet_id = fields.Many2one("hr.expense.sheet", "Expense Sheet")
