from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class sale_order_line_possibility(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.template", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute')

    @api.multi
    def _compute(self):
        for record in self:
            record.price = 1.0


class subline(Model):
    _inherit = 'sale.order.line'

    poss_ids = fields.One2many('sale.order.line.possibility', 'line_id', 'Possibilities')

    @api.model
    def create(self, values, context=None):
        record = super(subline, self).create(values)
        product_ids = record.product_id.alternative_product_ids
        poss = self.env['sale.order.line.possibility']
        for prod in product_ids:
            vals = {'line_id': record.id, 'product_id': prod.id}
            poss.create(vals)
        return record


    @api.onchange('product_id')
    @api.multi
    def write(self, values, context=None):
        record = super(subline, self).write(values)
        product_ids = self.product_id.alternative_product_ids
        poss = self.env['sale.order.line.possibility']
        if [poss.product_id for poss in self.poss_ids] != [prod for prod in product_ids]:
            self.poss_ids.unlink()
            for prod in product_ids:
                vals = {'line_id': self.id, 'product_id': prod.id}
                poss.create(vals)
        return record

