from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class ProductService(Component):
    _inherit = "base.rest.service"
    _name = "product.service"
    _usage = "product"
    _collection = "stock.rest.api.private.services"
    _description = """
        Product Services
        Access to the Product services is only allowed to authenticated users.
        If you are not authenticated please go to <a href='/web/login'>Login</a>
    """

    @restapi.method(
        [(["/get_product_qty_data"], "GET")],
        input_param=Datamodel("product.get.qty.param"),
    )
    def get_product_qty_data(self, values):
        """
        Payload example:
        {
            "values: {
                "product_ids": [5, 17]
                "lot_id": 7,
                "owner_id": 15,
                "package_id": 24,
                "from_date": "2024-01-09",
                "to_date": "2024-01-15",
            }
        }
        """

        values = values.values
        if "product_ids" not in values:
            return {}

        products = (
            self.env["product.product"]
            .browse(values["product_ids"])
            .filtered(lambda p: p.type != "service")
        )
        return products._compute_quantities_dict(
            values.get("lot_id", False),
            values.get("owner_id", False),
            values.get("package_id", False),
            values.get("from_date", False),
            values.get("to_date", False),
        )
