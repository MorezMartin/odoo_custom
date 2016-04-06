from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class tax_website_product(Model):
    _inherit = 'product.template'
    _name = 'product.template'

    tax_price = fields.Float(compute='_compute')

    @api.v8
    @api.multi
    @api.depends("taxes_id", "price")
    @api.model
    def _compute(self):
        for product in self:
            cur_obj = self.env["res.currency"]
            tax_obj = self.env["account.tax"]
            product.tax_price = product.taxes_id._unit_compute(product.taxes_id, product.price, product.id)
#            for taxes in tax_obj:
#                product.tax_price = product.order_id.pricelist_id.currency_id.round(taxes['amount'] / product.product_uom_qty)
