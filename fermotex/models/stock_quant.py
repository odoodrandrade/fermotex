# -*- coding: utf-8 -*-
from odoo import _, models, fields, api


class StockQuantInherith(models.Model):
    _inherit = 'stock.quant'

    quantity_fermo = fields.Float('Quantity', store=True)

    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        return ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id'] + self._get_inventory_fields_write()

    @api.model
    def _get_inventory_fields_write(self):
        """ Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
        """
        fields = ['inventory_quantity', 'inventory_quantity_auto_apply', 'inventory_diff_quantity',
                  'inventory_date', 'user_id', 'inventory_quantity_set', 'is_outdated', 'lot_id', 'quantity_fermo']
        return fields

    def action_apply_inventory(self):
        products_tracked_without_lot = []
        for quant in self:
            quant.lot_id.product_qty_fermo = quant.inventory_quantity
            quant.quantity_fermo = quant.quantity
            rounding = quant.product_uom_id.rounding
            if fields.Float.is_zero(quant.inventory_diff_quantity, precision_rounding=rounding) \
                    and fields.Float.is_zero(quant.inventory_quantity, precision_rounding=rounding) \
                    and fields.Float.is_zero(quant.quantity, precision_rounding=rounding):
                continue
            if quant.product_id.tracking in ['lot', 'serial'] and \
                    not quant.lot_id and quant.inventory_quantity != quant.quantity and not quant.quantity:
                products_tracked_without_lot.append(quant.product_id.id)
        # for some reason if multi-record, env.context doesn't pass to wizards...
        ctx = dict(self.env.context or {})
        ctx['default_quant_ids'] = self.ids
        quants_outdated = self.filtered(lambda quant: quant.is_outdated)
        if quants_outdated:
            ctx['default_quant_to_fix_ids'] = quants_outdated.ids
            return {
                'name': _('Conflict in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.inventory.conflict',
                'target': 'new',
                'context': ctx,
            }
        if products_tracked_without_lot:
            ctx['default_product_ids'] = products_tracked_without_lot
            return {
                'name': _('Tracked Products in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.track.confirmation',
                'target': 'new',
                'context': ctx,
            }
        self._apply_inventory()
        self.inventory_quantity_set = False
