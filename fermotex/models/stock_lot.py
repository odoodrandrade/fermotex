# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockLotInherith(models.Model):
    _inherit = 'stock.lot'

    product_qty_fermo = fields.Float('Quantity', store=True)

    @api.depends('quant_ids', 'quant_ids.quantity')
    def _product_qty(self):
        for lot in self:
            # We only care for the quants in internal or transit locations.
            quants = lot.quant_ids.filtered(lambda q: q.location_id.usage == 'internal' or (
                        q.location_id.usage == 'transit' and q.location_id.company_id))
            lot.product_qty = sum(quants.mapped('quantity'))
            lot.product_qty_fermo = lot.product_qty
