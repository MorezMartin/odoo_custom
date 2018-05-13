from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class sale_order_line_possibility(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.template", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute')

    def _compute(self):
        self.price = 1.0


class subline(Model):
    _inherit = 'sale.order.line'

    poss_ids = fields.One2many('sale.order.line.possibility', 'line_id', 'Possibilities')

    @api.model
    @api.depends('poss_ids')
    def create(self, values):
        record = super(subline, self).create(values)
        product_ids = self.product_id.alternative_product_ids
        poss = self.env['sale.order.line.possibility']
        for prod in product_ids:
            vals = {'line_id': self, 'product_id': prod}
            poss.create(vals)
        return record
