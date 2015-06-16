from openerp import fields, api
from openerp.models import Model

#TODO heriter une classe de sale.order et surcharger par une fonction
#qui remplacera les lignes (arguments) de mep_serv

#TODO ensuite dans la class mep_serv appeler la fonction de la class
#sale.order surchargee : comme on pourrait appeler compute_all pour
#les taxes


class mep_serv(Model):

    _name = "sale.mep_serv"

    name = fields.Char('Order Reference')
    date_order = fields.Datetime('Date')
    partner_id = fields.Many2one('Customer', compute='_compute')
#    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    def _compute(self):
        orders = self.env['sale.o'].search([('state', '=', 'done')])
        for order in orders:
            self.partner_id = order.make_mep(order)

class sale_o(Model):

    _name = "sale.o"
    _inherit = "sale.order"

    def make_mep(self, order):
        mep_vals = {
                'partner_id': order.partner_id.id
                }
        return mep_vals
