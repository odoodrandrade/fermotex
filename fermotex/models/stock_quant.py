# -*- coding: utf-8 -*-
from odoo import _, models, fields, api


class StockQuantInherith(models.Model):
    _inherit = 'stock.quant'

    quantity_fermo = fields.Float('Quantity', store=True)

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

    @api.model_create_multi
    def create(self, vals_list):
        """ Override to handle the "inventory mode" and create a quant as
        superuser the conditions are met.
        """
        quants = self.env['stock.quant']
        is_inventory_mode = self._is_inventory_mode()
        # allowed_fields = self._get_inventory_fields_create()
        for vals in vals_list:
            if is_inventory_mode and any(f in vals for f in ['inventory_quantity', 'inventory_quantity_auto_apply']):
                # if any(field for field in vals.keys() if field not in allowed_fields):
                #     raise UserError(_("Quant's creation is restricted, you can't do this operation."))
                auto_apply = 'inventory_quantity_auto_apply' in vals
                inventory_quantity = vals.pop('inventory_quantity_auto_apply', False) or vals.pop(
                    'inventory_quantity', False) or 0
                # Create an empty quant or write on a similar one.
                product = self.env['product.product'].browse(vals['product_id'])
                location = self.env['stock.location'].browse(vals['location_id'])
                lot_id = self.env['stock.lot'].browse(vals.get('lot_id'))
                package_id = self.env['stock.quant.package'].browse(vals.get('package_id'))
                owner_id = self.env['res.partner'].browse(vals.get('owner_id'))
                quant = self._gather(product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id,
                                     strict=True)
                if lot_id:
                    quant = quant.filtered(lambda q: q.lot_id)
                if quant:
                    quant = quant[0].sudo()
                else:
                    quant = self.sudo().create(vals)
                if auto_apply:
                    quant.write({'inventory_quantity_auto_apply': inventory_quantity})
                else:
                    # Set the `inventory_quantity` field to create the necessary move.
                    quant.inventory_quantity = inventory_quantity
                    quant.user_id = vals.get('user_id', self.env.user.id)
                    quant.inventory_date = fields.Date.today()
                quants |= quant
            else:
                quant = super().create(vals)
                quants |= quant
                if self._is_inventory_mode():
                    quant._check_company()
        return quants
