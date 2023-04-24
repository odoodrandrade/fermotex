# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date, datetime
from odoo import models, fields


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


    def action_print_statement(self):
        moves = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.move_id
        data = dict()
        lines = []
        report = []
        # Create default values.
        for move in self:

            # filtro para separar las vencidas de las vigentes
            is_expired = True
            if datetime.now().date().today() <= move.invoice_date_due:
                is_expired = False

            val = {
                'sequence_invoice': move.sequence_invoice,
                'name': move.name,
                'invoice_partner_display_name': move.invoice_partner_display_name,
                'partner_name': move.partner_id.name,
                'invoice_date': move.invoice_date,
                'invoice_date_due': move.invoice_date_due,
                'amount_total_signed': move.amount_total_signed,
                'payment_state': move.payment_state,
                'state': move.state,
                'is_expired': is_expired
            }
            lines.append(val)
        data['lines'] = lines
        lines.sort(reverse=False, key=lambda i: i['partner_name'])

        return self.env.ref(
            'fermotex.action_report_account_invoice_statement').report_action(
            self, data=data)

