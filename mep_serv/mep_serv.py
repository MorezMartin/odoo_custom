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

    @api.model
    def create_mep(self):
        mep = self.env['sale.mep_serv']
        mep_dic = {
                'name': self.name,
                'partner_id': self.partner_id.id,
                'date_order': self.date_order
                }
        return mep.create(mep_dic)


class sale_mep_serv(Model):

    _name = "sale.mep_serv"

    name = fields.Many2one('sale.order')
    partner_id = fields.Many2one('res.partner')
    date_order = fields.Datetime('Date')
