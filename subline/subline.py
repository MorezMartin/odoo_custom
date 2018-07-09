from openerp import fields, api
from openerp.models import Model
import openerp.addons.decimal_precision as dp

class sale_order_line_possibility(Model):
    _name = 'sale.order.line.possibility'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute')

    @api.multi
    @api.depends('line_id', 'product_id', 'line_id.order_id', 'line_id.order_id.pricelist_id', 'line_id.order_id.partner_id', 'line_id.product_uom', 'line_id.order_id.date_order')
    def _compute(self):
        for record in self:
            pricelist = record.line_id.order_id.pricelist_id
            partner = record.line_id.order_id.partner_id
            product = record.product_id
            price = self.env["product.pricelist"].with_context(date=record.line_id.order_id.date_order).price_get(product.id, 1, partner.id)#.with_context(date=line_id.order_id.date_order)
            record.price = price[pricelist.id]

class sale_order_line_option(Model):
    _name = 'sale.order.line.option'

    line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one("product.product", "Product", domain=[('sale_ok', '=', True)], readonly=True)
    price = fields.Float(compute='_compute')

    @api.multi
    @api.depends('line_id', 'product_id', 'line_id.order_id', 'line_id.order_id.pricelist_id', 'line_id.order_id.partner_id', 'line_id.product_uom', 'line_id.order_id.date_order')
    def _compute(self):
        for record in self:
            pricelist = record.line_id.order_id.pricelist_id
            partner = record.line_id.order_id.partner_id
            product = record.product_id
            price = self.env["product.pricelist"].with_context(date=record.line_id.order_id.date_order).price_get(product.id, 1, partner.id)#.with_context(date=line_id.order_id.date_order)
            record.price = price[pricelist.id]




class subline(Model):
    _inherit = 'sale.order.line'

    poss_ids = fields.One2many('sale.order.line.possibility', 'line_id', 'Possibilities')
    opt_ids = fields.One2many('sale.order.line.option', 'line_id', 'Options')

    @api.model
    def create(self, values, context=None):
        record = super(subline, self).create(values)
        product_poss_ids = record.product_id.possibilities
        product_opt_ids = record.product_id.options
        poss = self.env['sale.order.line.possibility']
        opt = self.env['sale.order.line.option']
        for prod in product_poss_ids:
            vals = {'line_id': record.id, 'product_id': prod.id}
            poss.create(vals)
        for prod in product_opt_ids:
            vals = {'line_id': record.id, 'product_id': prod.id}
            opt.create(vals)
        return record


    @api.onchange('product_id')
    @api.multi
    def write(self, values, context=None):
        record = super(subline, self).write(values)
        product_poss_ids = self.product_id.possibilities
        product_opt_ids = self.product_id.options
        poss = self.env['sale.order.line.possibility']
        opt = self.env['sale.order.line.option']
        if [poss.product_id for poss in self.poss_ids] != [prod for prod in product_poss_ids]:
            self.poss_ids.unlink()
            poss.unlink()
            for prod in product_poss_ids:
                vals = {'line_id': self.id, 'product_id': prod.id}
                poss.create(vals)
        if [opt.product_id for opt in self.opt_ids] != [opt for opt in product_opt_ids]:
            self.opt_ids.unlink()
            opt.unlink()
            for opt in product_opt_ids:
                vals = {'line_id': self.id, 'product_id': opt.id}
                opt.create(vals)
        return record

class product_template2(Model):
    _inherit = 'product.template'
    _name = 'product.template'

    possibilities = fields.Many2many('product.product', 'product_possibilities_rel', domain=[('sale_ok', '=', True)], readonly=False, string="Possibilities")
    options = fields.Many2many('product.product', 'product_options_rel', domain=[('sale_ok', '=', True)], readonly=False, string="Options")


    @api.multi
    def write(self, values):
        record = super(product_template2, self).write(values)
        sol = self.env['sale.order.line'].search([('product_id.product_tmpl_id', '=', self.id)])
        for line in sol:
            if ( line.mapped('poss_ids').mapped('product_id').sorted(key=lambda r:r.id) != self.possibilities.sorted(key=lambda r:r.id) ) or ( line.mapped('opt_ids').mapped('product_id').sorted(key=lambda r:r.id) != self.options.sorted(key=lambda r:r.id) ):
                line.write({'id': line.id})
        return record
