# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLineInherith(models.Model):
    _inherit = 'sale.order.line'

    qty_rolls = fields.Integer('Quantity rolls')
