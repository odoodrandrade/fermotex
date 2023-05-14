from odoo import models, fields, api, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    pw_available_lot_ids = fields.Many2many('stock.lot', compute='_compute_available_lot_ids', store=True)

    @api.depends('product_id', 'location_id', 'lot_id')
    def _compute_available_lot_ids(self):
        for rec in self:
            if rec.product_id and rec.location_id:
                quants = rec.env['stock.quant'].search([('lot_id', '!=', False), ('location_id', '=', rec.location_id.id), ('product_id', '=', rec.product_id.id)])
                rec.pw_available_lot_ids = quants.filtered(lambda x: (x.quantity - x.reserved_quantity) > 0).mapped('lot_id').ids
            else:
                rec.pw_available_lot_ids = [(6, 0, [])]
