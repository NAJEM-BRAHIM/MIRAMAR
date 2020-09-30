# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import fields, api, models, _

class CommissionLine(models.Model):
    _name = 'commission.lines'
    _rec_name = 'commission_name'
    _order = 'id desc'
    _description = "sales commission line"

    date = fields.Date(readonly=True)
    description = fields.Text(readonly=True)
    invoice_id = fields.Many2one('account.move', string="Invoice")
    user_id = fields.Many2one('res.users', string="Sales Person", readonly=True)
    sales_person_partner_id = fields.Many2one(related="user_id.partner_id", store=True, readonly=True)
    invoice_reference = fields.Char(readonly=True)
    order_reference = fields.Char(readonly=True)
    sale_commission = fields.Char(readonly=True)
    commission_name = fields.Char(readonly=True, required=True)
    commission_type = fields.Selection([
        ('standard', 'Standard'),
        ('partner', 'Partner Based'),
        ('product/category', 'Product/Category'),
    ], readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner", readonly=True)
    currency_id = fields.Many2one(related='user_id.currency_id', store=True, string='Currency', readonly=True)
    commission_amount = fields.Monetary(readonly=True)
    invoice_counter = fields.Integer(compute='compute_invoice_counter')

    @api.depends('invoice_id')
    def compute_invoice_counter(self):
        self.invoice_counter = len(self.invoice_id)


    def create_invoice(self):
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        other_account = self.env.ref('l10n_generic_coa.1_expense')
        result['context'] = {
            'default_type': 'in_invoice',
            'default_partner_id': self.sales_person_partner_id.id,
            'default_name': self.order_reference or self.invoice_reference,
            'default_invoice_date': fields.Date.today(),
            'default_line_ids': [(0, 0, {
                    'name': self.description,
                    'account_id': other_account and other_account.id or False,
                    'price_unit': self.commission_amount,
                    'exclude_from_invoice_tab': False,
                })],
        }
        res = self.env.ref('account.view_move_form', False)
        form_view = [(res and res.id or False, 'form')]
        if 'views' in result:
            result['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
        result['context']['default_origin'] = self.order_reference or self.invoice_reference
        result['context']['default_reference'] = self.order_reference or self.invoice_reference
        result['context']['from_commission'] = True
        return result

    def view_invoice(self):
        if self.invoice_id:
            invoices = self.mapped('invoice_id')
            action = self.env.ref('account.action_move_out_invoice_type').read()[0]
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
            return action