# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class AccountMoveInherith(models.Model):
    _inherit = 'account.move'
    sequence_invoice = fields.Char("Sequence fermotex", readonly=True, copy=False)
    state_secuence = fields.Selection(
        selection=[
            ('without_sequence', 'Without sequence'),
            ('with_sequence_f', 'With sequence invoice'),
            ('with_sequence_r', 'With sequence remision'),
        ],
        string='Status sequence',
        readonly=True,
        copy=False,
        default='without_sequence',
    )

    def action_sequence_fermotex(self):
        for records in self:
            records.sequence_invoice = "R/" + self.env['ir.sequence'].next_by_code('account.move.fermotex')
            records.state_secuence = 'with_sequence_r'

    def button_process_edi_web_services(self):
        res = super(AccountMoveInherith, self).button_process_edi_web_services()
        for records in self:
            records.sequence_invoice = "F/" + self.env['ir.sequence'].next_by_code('account.move.fermotex')
            records.state_secuence = 'with_sequence_f'
        return res
