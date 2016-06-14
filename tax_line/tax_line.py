from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class tax_line(Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    tax_price = fields.Float(compute='_compute')
    taxed_price = fields.Float(compute='_compute')
    tax_line = fields.Float(compute='_compute')
    taxed_line = fields.Float(compute='_compute')

    @api.v8
    @api.multi
    @api.depends("product_uom_qty", "product_id", "tax_id", "price_unit", "order_id.partner_id", "price_subtotal")
    @api.model
    def _compute(self):
        for line in self:
            cur_obj = self.env["res.currency"]
            tax_obj = self.env["account.tax"]
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            tax_obj = line.tax_id.compute_all(price, line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']
#            k = 0.0
            for taxes in tax_obj:
                line.tax_price = line.order_id.pricelist_id.currency_id.round(taxes['amount'] / line.product_uom_qty)
                line.taxed_price = line.order_id.pricelist_id.currency_id.round((taxes['amount'] / line.product_uom_qty) + price)
                line.taxed_line = line.order_id.pricelist_id.currency_id.round((line.product_uom_qty * line.taxed_price))
                line.tax_line = line.order_id.pricelist_id.currency_id.round(line.taxed_price - line.price_subtotal)
