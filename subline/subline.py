from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class sale_order_line_possibility(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute_price')


class subline(Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    poss_ids = fields.One2many('sale.order.line.possibility', 'line_id', 'Possibilities', compute='_computeo2m')

    @api.v8
    @api.multi
#    @api.depends("product_id")
    @api.model
    def _computeo2m(self):
        for product in self.product_id.alternative_product_ids:
            for poss in poss_ids:
                poss.line_id = self.id
                poss.product_id = product
                poss.price = 1.0


