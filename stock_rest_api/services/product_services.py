import ast
from datetime import datetime
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class ProductService(Component):
    _inherit = "product.service"
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
            "values": {
                "product_ids": "[5, 17]",
                "lot_id": 7,
                "owner_id": 15,
                "package_id": 24,
                "from_date": "2024-01-09",
                "to_date": "2024-01-15",
            }
        }
        """

        values = values.values

        if "product_ids" not in values or not values["product_ids"]:
            return {"error": "Missing product_ids"}, 400

        try:
            product_list = ast.literal_eval(str(values["product_ids"]))
            if not isinstance(product_list, list):
                raise ValueError
        except (ValueError, SyntaxError):
            return {"error": "Invalid format for product_ids."}, 400

        from_date = values.get("from_date")
        to_date = values.get("to_date")
        try:
            if from_date:
                datetime.strptime(from_date, "%Y-%m-%d")
            if to_date:
                datetime.strptime(to_date, "%Y-%m-%d")
            if from_date and to_date and from_date > to_date:
                return {"error": "from_date cannot be later than to_date"}, 400
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

        product_obj = self.env["product.product"]

        if not product_list:
            products = product_obj.search([])
        else:
            products = product_obj.browse(product_list)
            if not products:
                return {"error": "No products found with the provided IDs"}, 404

        filtered_products = products.filtered(lambda p: p.type != "service")
        if not filtered_products:
            return {"error": "All selected products are of type 'service'"}, 404

        try:
            quantities = filtered_products._compute_quantities_dict(
                values.get("lot_id", False),
                values.get("owner_id", False),
                values.get("package_id", False),
                from_date,
                to_date,
            )
        except Exception as e:
            return {"error": str(e)}, 500

        return quantities, 200
