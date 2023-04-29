# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplateInherith(models.Model):
    _inherit = 'product.template'

    def fermo_action_open_product_lot(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("fermotex.fermo_action_production_lot_form")
        action['domain'] = [('product_id.product_tmpl_id', '=', self.id)]
        action['context'] = {
            'default_product_tmpl_id': self.id,
            'default_company_id': (self.company_id or self.env.company).id,
        }
        if self.product_variant_count == 1:
            action['context'].update({
                'default_product_id': self.product_variant_id.id,
            })
        return action


class ProductProductInherith(models.Model):
    _inherit = 'product.product'

    def fermo_action_open_product_lot(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("fermotex.fermo_action_production_lot_form")
        action['domain'] = [('product_id', '=', self.id)]
        action['context'] = {
            'default_product_id': self.id,
            'set_product_readonly': True,
            'default_company_id': (self.company_id or self.env.company).id,
        }
        return action
