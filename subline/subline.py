from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class sale_order_line_possibility(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute')

    def _compute(self):
        self.price = 1.0


class subline(Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    poss_ids = fields.One2many('sale.order.line.possibility', 'line_id', 'Possibilities')

    @api.model
    def create(self, values):
        record = super(sale_order_line, self).create(values)
        product_ids = self.product_id.alternative_product_ids
        vals = {}
        poss = self.env['sale.order.line.possibility']
        for prod in product_ids:
            vals = {'line_id': self.id, 'product_id': prod.id}
            poss.create(vals)
        return record
