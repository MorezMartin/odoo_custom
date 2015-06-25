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

    @api.multi
    def create_mep(self):
        mep = self.env['sale.mep_serv']
        mep_dic = {}
        for order in self:
            mep_dic = {
                'name': order.id,
                'partner_id': order.partner_id.id,
                'date_order': order.date_order,
                }
        res = mep.create(mep_dic)
        return res

    @api.multi
    def action_button_confirm(self):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.signal_workflow(cr, uid, ids, 'order_confirm')
        self.create_mep()
        return True


class sale_mep_serv(Model):

    _name = "sale.mep_serv"

    name = fields.Many2one('sale.order', string='Reference')
    partner_id = fields.Many2one('res.partner')
    date_order = fields.Datetime('Date')
