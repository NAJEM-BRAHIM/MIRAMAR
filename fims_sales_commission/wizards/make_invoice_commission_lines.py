# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'commission.lines.create.inv'
    _description = 'commission lines create inv'

    def _default_get_ids(self):
        return self.env['commission.lines'].browse(self._context.get('active_ids'))

    active_ids = fields.Many2many('commission.lines', default=_default_get_ids, invisible=True)
    group_by = fields.Boolean(string="Group BY")

    def create_invoice(self):
        if self.group_by:
            self._create_invoice()
        else:
            invoice = ''
            for id in self.active_ids:
                AccountInvoice = self.env['account.move']
                if not id.invoice_id:
                    invoice = AccountInvoice.create({
                        'type': 'in_invoice',
                        'partner_id': id.sales_person_partner_id.id,
                        'invoice_date': fields.Date.today(),
                        #'account_id': id.partner_id.property_account_receivable_id.id,
                        'invoice_line_ids': [(0, 0, {
                            'name': id.description,
                            'account_id': id.partner_id.property_account_receivable_id.id,
                            'name': id.order_reference or id.invoice_reference,
                            'price_unit': id.commission_amount,
                            'price_subtotal': id.commission_amount,
                        })]
                    })
                    id.invoice_id = invoice.id
            return invoice


    def _create_invoice(self):
        commission_lines = self.env['commission.lines'].read_group([('id', 'in', self.env.context.get('active_ids'))],
                                                          ['description', 'order_reference', 'invoice_reference', 'commission_amount', 'user_id'],
                                                          'user_id')
        for commission_line in commission_lines:
            domain = commission_line['__domain']
            domain.append(('invoice_id', '=', False))
            lines = self.env['commission.lines'].search(domain)
            AccountInvoice = self.env['account.move']
            if lines:
                invoice = AccountInvoice.create({
                    'type': 'in_invoice',
                    'partner_id': lines[0].sales_person_partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'account_id': lines[0].partner_id.property_account_receivable_id.id,
                })
                for line in lines:
                    invoice.update({
                        'invoice_line_ids': [(0, 0, {
                            'name': line.description,
                            'account_id': line.partner_id.property_account_receivable_id.id,
                            'name': line.order_reference or line.invoice_reference,
                            'price_unit': line.commission_amount,
                            'price_subtotal': line.commission_amount,
                        })]
                    })
                    line.invoice_id = invoice.id

