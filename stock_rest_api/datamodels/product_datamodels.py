from marshmallow import fields
from odoo.addons.datamodel.core import Datamodel


class ProductGetStockQty(Datamodel):
    _name = "product.get.qty.param"
    _description = "Product Get Stock Qty Param"

    values = fields.Dict(required=True, allow_none=False)
