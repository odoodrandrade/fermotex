from odoo import models, fields, api, _


class SaleOrderInherith(models.Model):
    _inherit = 'sale.order'

    delivery_street = fields.Char(string="Domicilio de entrega", compute='compute_delivery_street', store=True)

    @api.depends('warehouse_id')
    def compute_delivery_street(self):
        for rec in self:
            rec.delivery_street = rec.warehouse_id.partner_id.contact_address_complete
            print(rec.warehouse_id.partner_id.contact_address)