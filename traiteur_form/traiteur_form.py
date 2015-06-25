from openerp import fields, api
from openerp.models import Model

class traiteur_form(Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    horaire_fin = fields.Datetime('Horaire de fin', required=True)
    type_presta = fields.Char('Type de prestation', required=True)
    couleur_deco = fields.Char('Couleur Decoration')
    noms = fields.Char('Noms et Prenoms (prestation particulier)')
    demandes_supp = fields.Text('Demandes supplementaires')

class sale_o_l(Model):
    _inherit = 'sale.order.line'
    _name = 'sale.order.line'

    timing = fields.Datetime('Timing')

    @api.multi
    def _get_date_order(self):
        res = self.order_id.date_order
        return res

    _defaults = {
            'timing': _get_date_order
            }

