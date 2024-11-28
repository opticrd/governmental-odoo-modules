from odoo import models, fields


class ProductPriceHistory(models.Model):
    _name = "product.price.history"
    _description = "Product Price History"
    _rec_name = "date"
    _order = "date, product_id"

    date = fields.Date(index=True, readonly=True, required=True)
    product_id = fields.Many2one(
        "product.product", "Product", index=True, readonly=True, required=True
    )
    default_code = fields.Char(
        "Internal Reference",
        related="product_id.default_code",
        store=True,
        readonly=True,
    )
    po_uom_id = fields.Many2one(
        "uom.uom",
        "Purchase Unit of Measure",
        index=True,
        readonly=True,
    )
    prd_uom_id = fields.Many2one(
        "uom.uom",
        "Product Unit of Measure",
        related="product_id.uom_id",
        store=True,
        index=True,
        readonly=True,
    )
    categ_id = fields.Many2one(
        "product.category",
        "Category",
        related="product_id.categ_id",
        store=True,
        index=True,
        readonly=True,
    )
    company_po_price_unit = fields.Monetary(
        "Cost on Purchase",
        readonly=True,
        required=True,
        currency_field="company_currency_id",
        help="Unit price from purchase line unit of measure in company currency",
    )
    company_prd_price_unit = fields.Monetary(
        "Cost by Unit",
        readonly=True,
        required=True,
        currency_field="company_currency_id",
        help="Unit price from product base unit of measure in company currency",
    )
    currency_po_price_unit = fields.Monetary(
        "Currency Cost on Purchase",
        readonly=True,
        currency_field="purchase_currency_id",
        help="Unit price from purchase line unit of measure in PO currency",
    )
    currency_prd_price_unit = fields.Monetary(
        "Currency Cost by Unit",
        readonly=True,
        currency_field="purchase_currency_id",
        help="Unit price from product base unit of measure in PO currency",
    )
    purchase_id = fields.Many2one(
        "purchase.order", "Purchase Order", index=True, readonly=True
    )
    purchase_line_id = fields.Many2one(
        "purchase.order.line",
        "Purchase Order Line",
        index=True,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", "Vendor", index=True, readonly=True)
    account_id = fields.Many2one(
        "account.account",
        "Account",
        related="product_id.property_account_expense_id",
        store=True,
        index=True,
        readonly=True,
    )
    state = fields.Selection(
        [("draft", "Draft"), ("purchase", "Confirmed"), ("cancel", "Cancelled")],
        required=True,
        index=True,
        default="draft",
        help="* Draft: Manually (import) created,"
        "* Confirmed: Origin Purchase Order was confirmed,"
        "* Cancelled: Origin Purchase Order was cancelled.",
    )
    company_currency_id = fields.Many2one(
        "res.currency", "Company Currency", readonly=True
    )
    purchase_currency_id = fields.Many2one(
        "res.currency", "Purchase Currency", readonly=True
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        readonly=True,
        index=True,
        default=lambda self: self.env.company,
    )
