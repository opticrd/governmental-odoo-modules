# -*- coding: utf-8 -*-
"""
Fleet Method Payment Module.

This module defines the Odoo model for managing payment methods related to the fleet of vehicles.
It includes the definition of the 'FleetPaymentMethod' class, which represents a payment method
used for managing transactions related to the fleet.

:model: fleet.payment.method
:author: Estarling Polanco <jesus.polanco@economia.gob.do>
"""
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FleetPaymentMethod(models.Model):
    """
    This model represents a payment method used for managing transactions
    related to the fleet of vehicles. It includes information such as the
    journal, account number, bank name, and other relevant details.
    """

    _name = "fleet.payment.method"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Record Payment Method"

    _sql_constraints = [
        ("number_uniq", "unique (acc_number)", "This account number already exists!")
    ]

    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        domain="[('type', '=', 'bank'), ('l10n_do_payment_form', '=', 'card')]",
    )
    account_type = fields.Selection(
        string="Type", related="journal_id.type", readonly=True
    )
    payment_form = fields.Selection(
        string="Payment Form", related="journal_id.l10n_do_payment_form", readonly=True
    )
    acc_number = fields.Char(
        string="Account Number",
        related="journal_id.bank_account_id.acc_number",
        readonly=True,
        store=True,
    )
    bank_name = fields.Char(
        string="Bank Name", related="journal_id.bank_id.name", readonly=True
    )
    cutoff_date = fields.Integer(
        "Cutting day",
        required=True,
        tracking=True,
        help="Enter the day of the month (1-31)",
    )
    due_date = fields.Char(string="Due Date", required=True, tracking=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("active", "Active"),
            ("expired", "Expired"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="new",
        tracking=True,
    )

    def action_validate(self):
        """
        This method sets the state of the payment method to 'active', indicating
        that it has been validated and is ready for use.
        """
        self.write({"state": "active"})

    def action_cancel(self):
        """
        This method sets the state of the payment method to 'cancel', indicating
        that it has been canceled and should not be used.
        """
        self.write({"state": "cancel"})

    def get_acc_number_short(self, acc_number):
        """
        Method to get the short number or 'XXXXXX' if there is no account number.
        """
        return acc_number[-6:] if acc_number else "XXXXXX"

    def name_get(self):
        """
        This method is used to provide a human-readable name for each record
        in the user interface.

        Return a list of tuples containing the ID and a string representation
        for each record in the set.
        """
        return [
            (
                acc.id,
                f"{acc.payment_form if acc.payment_form else 'No Payment Form'} - "
                f"{self.get_acc_number_short(acc.acc_number)}",
            )
            for acc in self
        ]

    @api.constrains("due_date")
    def _check_due_date_format(self):
        """
        This method is a constraint that validates the format of the 'due_date'
        field. It ensures that the date follows the format MM/YYYY.
        """
        for record in self:
            if record.due_date:
                self._validate_date_format(record.due_date)

    @staticmethod
    def _validate_date_format(date):
        """
        This static method checks if the provided date string follows the format MM/YYYY.
        If the format is incorrect, it raises a ValidationError.
        """
        if date is not None:
            error = _("Error. Date format must be MM/YYYY")
            if len(date) == 7:
                try:
                    datetime.strptime(date, "%m/%Y")
                except ValueError as exc:
                    raise ValidationError(error) from exc
            else:
                raise ValidationError(error)
