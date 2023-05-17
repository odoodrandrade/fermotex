from odoo import models


class StockMoveInherith(models.Model):
    _inherit = 'stock.move'

    def _compute_show_details_visible(self):
        res = super(StockMoveInherith, self)._compute_show_details_visible()
        for move in self:
            if move.product_id:
                move.show_details_visible = True
        return res
