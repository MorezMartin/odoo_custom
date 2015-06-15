from openerp import fields
from openerp.models import Model

class traiteur_form(Model):
    _inherit = 'sale.order'
    _name = 'sale.order'

    horaire_fin = fields.Datetime('Horaire de fin', required=True)
    type_presta = fields.Char('Type de prestation', required=True)
    couleur_deco = fields.Char('Couleur Decoration')
    noms = fields.Char('Noms et Prenoms (prestation particulier)')
    demandes_supp = fields.Text('Demandes supplementaires')

#traiteur_form()
