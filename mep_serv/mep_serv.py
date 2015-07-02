from openerp import fields, api
from openerp.models import Model

#TODO heriter une classe de sale.order et surcharger par une fonction
#qui remplacera les lignes (arguments) de mep_serv

#TODO ensuite dans la class mep_serv appeler la fonction de la class
#sale.order surchargee : comme on pourrait appeler compute_all pour
#les taxes


class sale_o_l(Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    timing = fields.Datetime("Timing")


class sale_o(Model):

    _name = "sale.order"
    _inherit = "sale.order"

    type_presta = fields.Char("Type Presta")
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


#TODO : mettre a jour mep_dic et que confirm cree les mep
    @api.multi
    def create_mep(self):
        mep = self.env['sale.mep_serv']
        mep_dic = {}
        mep_l_dic = {}
        for order in self:
            mep_dic = {
                'name': order.id,
                'partner_id': order.partner_id.id,
                'date_order': order.date_order,
                'state': order.state,
                'partner_shipping_id': order.partner_shipping_id.id
                }
        res = mep.create(mep_dic)
        return res, self.create_mep_lines()

    @api.multi
    def create_mep_lines(self):
        lines = []
        mep_l = self.env['sale.mep_serv.line']
        for line in self.order_line:
            lines.append(line)
        res = mep_l.create(lines)
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

class sale_mep_l(Model):
    _name="sale.mep_serv.line"

    order_id = fields.Many2one('sale.order', 'Order Reference')
    name = fields.Text('Description')
    product_id = fields.Many2one('product.product', 'Product')


class sale_mep_serv(Model):

    _name = "sale.mep_serv"


    name = fields.Many2one('sale.order')
    date_order = fields.Datetime("Date")
    type_presta = fields.Char("Type Presta")
    mep_line = fields.One2many('sale.mep_serv.line', 'order_id')
    partner_shipping_id = fields.Many2one('res.partner')
    partner_id = fields.Many2one('res.partner')
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
    def _compute_line(self):
        res = self.env['sale.order'].create_mep_lines()
        return res

    @api.multi
    def print_mep(self):
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time.'
        res = self.env['report'].get_action(self, 'mep_serv.report_mep')
        return res
