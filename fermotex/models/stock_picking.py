from odoo import models, fields, api, _


class PickingInherith(models.Model):
    _inherit = 'stock.picking'

    def action_report_delivery(self):
        self.write({'printed': True})
        if any("MEZCLILLA" in record.product_id.name for record in self.move_line_ids):
            # Acción si al menos un producto contiene "MEZCLILLA" en el nombre
            return self.env.ref('fermotex.action_report_picking_pantalon').report_action(self)
        else:
            # Acción si ningún producto contiene "MEZCLILLA" en el nombre
            return self.env.ref('stock.action_report_picking').report_action(self)
