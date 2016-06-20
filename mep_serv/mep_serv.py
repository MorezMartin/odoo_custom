from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp



class sale_o_l(Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    @api.multi
    def _get_date_order(self):
        res = self.order_id.date_order
        return res

    timing = fields.Datetime('Timing', default=_get_date_order)
    name = fields.Text('Description', required=True, readonly=False, states={'draft': [('readonly', False)]})   
    product_id = fields.Many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True, readonly=False, states={'draft': [('readonly', False)]}, ondelete='restrict')

    price_unit = fields.Float('Unit Price', required=True, digits_compute=dp.get_precision('Product Price'), readonly=False, states={'draft': [('readonly', False)]})
    product_uom_qty = fields.Float('Quantity', digits_compute=dp.get_precision('Product UoS'), required=True, readonly=False, states={'draft': [('readonly', False)]})

class sale_o(Model):

    _name = "sale.order"
    _inherit = "sale.order"


    order_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)], 'reserved': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True)
    horaire_fin = fields.Datetime('Horaire de fin', required=True, default=fields.Datetime.now)
    date_order = fields.Datetime('Date', required=True, readonly=True, select=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'reserved': [('readonly', False)],}, copy=True),
    type_presta = fields.Selection([
        ('mar', 'Mariage Complet'),
        ('vh', 'Vin d\'honneur'),
        ('marr', 'Repas Mariage'),
        ('cock', 'Cocktail'),
        ('cockplat', 'Cocktail et plat au buffet'),
        ('rent', 'Repas d\'entreprise soiree festive'),
        ('anniv', 'Anniversaire'),
        ('com', 'Communion'),
        ('bapt', 'Bapteme'),
        ('annivm', 'Anniversaire de mariage'),
        ('sem', 'Seminaire'),
        ('cong', 'Congres'),
        ('rasso', 'Repas associatif'),
        ('autre', 'Autre')
        ], required=True, select=True, default='mar')
    couleur_deco = fields.Char('Couleur Decoration')
    noms = fields.Char('Noms et Prenoms (prestation particulier)')
    demandes_supp = fields.Text('Demandes supplementaires')
    state = fields.Selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('reserved', 'Reserved'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True)
    fst_advance = fields.Float('Premier acompte')
    scd_advance = fields.Float('Deuxieme acompte')
    trd_advance = fields.Float('Troisieme acompte')
    to_pay = fields.Float(compute='_to_pay')


    @api.multi
    def _to_pay(self):
        total = self.amount_total
        self.to_pay = self.amount_total - self.fst_advance - self.scd_advance - self.trd_advance

    @api.multi
    def action_button_confirm(self):
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time.'
        self.signal_workflow('order_confirm')
        return True

    @api.multi
    def action_button_reserv(self):
        self.state = 'reserved'
        return True

    @api.multi
    def print_mep(self):
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        return self.env['report'].get_action(self, 'mep_serv.report_mep')
