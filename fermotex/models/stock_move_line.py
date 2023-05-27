# -*- coding: utf-8 -*-
from odoo import _, api, fields, tools, models
from odoo.exceptions import UserError


class StockMoveLineInherith(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('lot_id')
    def on_lot_id_change(self):
        for record in self:
            record.qty_done = record.lot_id.product_qty

    @api.ondelete(at_uninstall=False)
    def _unlink_except_done_or_cancel(self):
        for ml in self:
            if ml.state in 'cancel':
                raise UserError(_('You can not delete product moves if the picking is done. You can only correct the done quantities.'))