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

    type_presta = fields.Char("Type Prestation")
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
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time.'
        self.signal_workflow('order_confirm')
        self.create_mep()
        return True

    @api.multi
    def action_button_reserv(self):
        self.state = 'reserved'
        return True

    @api.multi
    def print_mep(self):
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time.'
        res = self.env['report'].get_action('mep_serv.report_mep')
        return res


class sale_mep_serv(Model):

    _name = "sale.mep_serv"

    name = fields.Many2one('sale.order', string='Reference')
    partner_id = fields.Many2one('res.partner')
    date_order = fields.Datetime('Date')
