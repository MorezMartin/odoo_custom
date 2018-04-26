from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class subline(Model):
    _inherit = 'sale.order.line'

    possibilities = fields.One2many(comodel_name = 'sale.order.line.possibility', inverse_name = 'line_id', 'Possibilities', readonly=True, compute='_computeo2m')
#    options = fields.One2many('sale.order.line.options', 'line_id', "Options", readonly=True)

    @api.v8
    @api.multi
    @api.depends("product_id")
    @api.model
    def _computeo2m(self):
        for poss, product in self.possibility, self.product_id.alternative_product_ids:
            poss.product_id = product


def possibilities(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.subline', readonly=True)
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute_price')

    @api.v8
    @api.multi
#    @api.depends("product_id")
    @api.model
    def _compute_price(self):
        for poss in self:
            poss.price = 1.0


