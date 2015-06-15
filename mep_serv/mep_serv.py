from openerp import fields, api
from openerp.models import Model

#creer automatiquement plusieurs lignes d'enregistrements definies dans code
#essayer d'abord avec valeurs fixes
#ensuite essayer avec valeurs heritees de sale.order

class mep_serv(Model):
    _name = "sale.mep_serv"

    name = fields.Char('Order Reference')
    date_order = fields.Datetime('Date')
    partner_id = fields.Many2one( 'Customer', compute='_compute')
#    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.v8
    @api.multi
    @api.depends('sale.order')
    @api.model
    def _compute(self):
        domain = [('state', '=', ('done'))] 
        sos = []#self.env['sale.order'].search([domain])
        for so in sos:
            for mep in self:
                mep.partner_id = so.partner_id

