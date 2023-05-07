# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLineInherith(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('lot_id')
    def on_lot_id_change(self):
        for record in self:
            record.qty_done = record.lot_id.product_qty
