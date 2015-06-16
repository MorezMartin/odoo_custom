from openerp import fields, api
from openerp.models import Model

#TODO heriter une classe de sale.order et surcharger par une fonction
#qui remplacera les lignes (arguments) de mep_serv

#TODO ensuite dans la class mep_serv appeler la fonction de la class
#sale.order surchargee : comme on pourrait appeler compute_all pour
#les taxes


class sale_o(Model):

    _name = "sale.order"
    _inherit = "sale.order"

    def prepare_mep(self):
        orders = self.search([('state', 'in', ['confirmed'])])
        for order in orders:
            mep_list = []
            mep_vals = {
                'partner_id': order.partner_id.id,
                'date_order': order.date_order,
                'name': order.name
                    }
            mep_list.append(mep_vals)
        return mep_list

    def make_mep(self):
        mep_l = self.prepare_mep()
        m = self.env['sale.mep_serv']
        for mep in mep_l:
            m.create(mep)


class mep_serv(Model):

    _name = "sale.mep_serv"

    name = fields.Char('Order Reference')
    date_order = fields.Datetime('Date')
    partner_id = fields.Many2one('res.partner', 'Customer', compute='_compute')
#    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    def _compute(self):
        orders = self.env['sale.order']
        orders.make_mep()
