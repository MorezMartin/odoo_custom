from openerp import fields, api
from openerp.models import Model

#creer automatiquement plusieurs lignes d'enregistrements definies dans code
#essayer d'abord avec valeurs fixes
#ensuite essayer avec valeurs heritees de sale.order


class mep_serv(Model):
    _name = "sale.mep_serv"

    name = fields.Char('Order Reference')
    date_order = fields.Datetime('Date')
    partner_id = fields.Many2one('res.partner', 'Customer')
#    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    def _compute(self):
        for so in self :
            so.name = "test"

    @api.model
    @api.returns
    def create(self):
        return env[self].create(name="test")
