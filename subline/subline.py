from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class sale_order_line_possibility(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)], readonly=True, compute='_compute')
    price = fields.Float(compute='_compute')

    def _compute(self):
        products = self.env['product.product'].search([])#.browse(line_id.product_id.alt_ids)
        for product in products:
            self.product_id = product.id
            self.price = 1.0


class subline(Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    poss_ids = fields.One2many('sale.order.line.possibility', 'line_id', 'Possibilities')

#TODO TESTER affichage produits directement dans subline via compute, puis voir le reste après
