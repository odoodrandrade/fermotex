from odoo import models, fields, api, _


class SaleOrderInherith(models.Model):
    _inherit = 'sale.order'

    delivery_street = fields.Char(string="Domicilio de entrega", compute='compute_delivery_street', store=True)

    state = fields.Selection(
        selection=[
            ('draft', "Quotation"),
            ('sent', "Quotation Sent"),
            ('to-auth', "To authorize"),
            ('rejected', "Rejected"),
            ('authorized', "Authorized"),
            ('sale', "Sales Order"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    need_auth = fields.Boolean(string="Need auth", compute='_compute_has_to_be_confirm', store=True)

    def action_authorize(self):
        for records in self:
            records.write({'state': 'authorized'})

    def action_reject(self):
        for records in self:
            records.write({'state': 'rejected'})

    @api.depends('warehouse_id')
    def compute_delivery_street(self):
        for rec in self:
            rec.delivery_street = rec.warehouse_id.partner_id.contact_address_complete
            print(rec.warehouse_id.partner_id.contact_address)

    @api.depends('order_line.price_subtotal')
    def _compute_has_to_be_confirm(self):
        need_authorization = False
        for lines in self.order_line:
            if lines.price_unit < lines.product_id.list_price:
                need_authorization = True
        self.need_auth = need_authorization
        if need_authorization is False:
            self.write({'state': 'authorized'})
        else:
            self.write({'state': 'to-auth'})

    def action_confirm(self):
        res = super(SaleOrderInherith, self.with_context(default_immediate_transfer=True)).action_confirm()
        for order in self:
            if order.picking_ids:
                for picking in self.picking_ids:
                    for move_lines in picking.move_line_ids:
                        move_lines.unlink()
        return res
