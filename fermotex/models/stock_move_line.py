# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLineInherith(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('reserved_uom_qty')
    def _update_qty(self):
        for record in self:
            print(record)
