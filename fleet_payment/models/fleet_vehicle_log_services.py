# -*- coding: utf-8 -*-
"""
Fleet Vehicle Log Services Module.

This module extends the 'fleet.vehicle.log.services' model in Odoo. It introduces additional
fields and functionalities related to fleet services. It includes enhancements such as recording
the license plate, brand, model, payment method, and reference for a fleet service log.

:model: fleet.vehicle.log.services
:author: Estarling Polanco <jesus.polanco@economia.gob.do>
"""
from odoo import models, fields


class FleetVehicleLogServices(models.Model):
    """
    Extends the Odoo model 'fleet.vehicle.log.services' with additional fields.
    """

    _inherit = "fleet.vehicle.log.services"

    license_plate = fields.Char(
        string="Plate", related="vehicle_id.license_plate", readonly=True
    )
    brand = fields.Char(
        string="Brand", related="vehicle_id.model_id.brand_id.name", readonly=True
    )
    model = fields.Char(
        string="Model", related="vehicle_id.model_id.name", readonly=True
    )
    payment_method_id = fields.Many2one(
        "fleet.payment.method",
        string="Method Payment",
        domain=[("state", "=", "active")],
        help="Select the payment method",
    )
    ref = fields.Char(string="Reference")
