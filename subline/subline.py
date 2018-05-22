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
    def create(self, values, context=None):
        record = super(subline, self).create(values)
        product_ids = self.product_id.alternative_product_ids
        poss = self.poss_ids
        line_id = self.id
        for prod in product_ids:
            vals = {'line_id': line_id, 'product_id': prod.id}
            poss.create(vals)
        return record


    @api.multi
    def write(self, values, context=None):
        record = super(subline, self).write(values)
        product_ids = self.product_id.alternative_product_ids
        poss = self.poss_ids
        line_id = self.id
        for prod in product_ids:
            vals = {'line_id': line_id, 'product_id': prod.id}
            poss.write(vals)
        return record
