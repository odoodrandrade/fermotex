from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError


class SaleOrderInherith(models.Model):
    _inherit = 'sale.order'

    delivery_street = fields.Char(string="Domicilio de entrega", compute='compute_delivery_street', store=True)

    @api.depends('warehouse_id')
    def compute_delivery_street(self):
        for rec in self:
            rec.delivery_street = rec.warehouse_id.partner_id.contact_address_complete
            print(rec.warehouse_id.partner_id.contact_address)
            

    def action_confirm(self):
        for rec in self:
            if not rec.env.user.has_group("fermotex.group_allow_confirm_unlock_so"):
                raise AccessError(_("You are not allowed to confirm orders, please contact your system administrator."))
        return super(SaleOrderInherith, self).action_confirm()
