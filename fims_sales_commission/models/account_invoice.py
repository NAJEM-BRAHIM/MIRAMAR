# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    sales_commission_ids = fields.One2many('sales.commission.invoice.line', 'sales_invoice_id', readonly=True)

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if self._context.get('from_commission'):
            comm_line = self.env['commission.lines'].browse(self._context.get('active_id'))
            comm_line.invoice_id = res.id
        return res

    def action_post(self):
        invoice = super(AccountMove, self).action_post()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        if get_param('fims_sales_commission.commission_based_on') == 'invoice':
            self.generate_sales_commission()
        return invoice

    def calculate_commission(self, amount, discount):
        return (amount * discount) / 100


    def generate_sales_commission(self):
        commission = 0
        sales_commission = self.env['sales.commission'].search([('user_id', '=', self.user_id.id)], limit=1)
        if sales_commission.commission_type == "standard":
            commission = self.calculate_commission(self.amount_untaxed,
                                                   sales_commission.standard_commission_percentage)
            percentage = sales_commission.standard_commission_percentage
            description = 'standard'
            self.confirm_sales_commission(commission, sales_commission, percentage, description)
        elif sales_commission.commission_type == "partner":
            if self.partner_id.affiliated:
                commission = self.calculate_commission(self.amount_untaxed,
                                                       sales_commission.affiliated_partner_commission)
                percentage = sales_commission.affiliated_partner_commission
                description = 'Affiliated Partner'
                self.confirm_sales_commission(commission, sales_commission, percentage, description)
            else:
                commission = self.calculate_commission(self.amount_untaxed,
                                                       sales_commission.non_affiliated_partner_commission)
                percentage = sales_commission.non_affiliated_partner_commission
                description = 'Non Affiliated Partner'
                self.confirm_sales_commission(commission, sales_commission, percentage, description)
        elif sales_commission.commission_type == "product/category":
            for line in sales_commission.product_category_lines:
                if line.based_on == 'product':
                    get_category_ids = sales_commission.product_category_lines.mapped('category_id')
                    for invoice_line in self.invoice_line_ids:
                        if invoice_line.product_id == line.product_id:
                            if line.product_id.categ_id in get_category_ids:
                                pass
                            else:
                                if line.with_commission == 'fix price':
                                    if invoice_line.price_subtotal > line.target_price:
                                        commission = self.calculate_commission(invoice_line.price_subtotal,
                                                                               line.above_price_commission)
                                        percentage = line.above_price_commission
                                        description = line.product_id.name
                                        self.confirm_sales_commission(commission, sales_commission, percentage, description)
                                else:
                                    commission = self.calculate_commission(invoice_line.price_subtotal,
                                                                           line.commission)
                                    percentage = line.commission
                                    description = line.product_id.name
                                    self.confirm_sales_commission(commission, sales_commission, percentage, description)
                else:
                    for invoice_line in self.invoice_line_ids:
                        if invoice_line.product_id.categ_id == line.category_id:
                            if line.with_commission == 'fix price':
                                if invoice_line.price_subtotal > line.target_price:
                                    commission = self.calculate_commission(invoice_line.price_subtotal,
                                                                           line.above_price_commission)
                                    percentage = line.above_price_commission
                                    description = line.category_id.name
                                    self.confirm_sales_commission(commission, sales_commission, percentage, description)
                            else:
                                commission = self.calculate_commission(invoice_line.price_subtotal,
                                                                       line.commission)
                                percentage = line.commission
                                description = line.category_id.name
                                self.confirm_sales_commission(commission, sales_commission, percentage, description)


    def confirm_sales_commission(self, commission, sales_commission, percentage, description):
        invoice_type = self.type
        invoice_modify = self.env.context.get('invoice_modify')
        amount=commission
        if commission:
            add_discription = sales_commission.commission_type + ' " ' + sales_commission.name + ' " ' + "(" + str(percentage) + "%" + ") " + str(description)
            if invoice_type == 'out_invoice' and not invoice_modify:
                amount = commission
            if invoice_type == 'out_invoice' and invoice_modify:
                amount = -(commission)
            if commission and invoice_type == 'out_refund':
                amount = -(commission)
            self.write({'sales_commission_ids': [(0, 0, {'date': fields.Date.today(),
                                                         'description': add_discription,
                                                         'commission_type': sales_commission.commission_type,
                                                         'name': sales_commission.name,
                                                         'user_id': self.user_id.id,
                                                         'commission_amount': amount
                                                         })]})
            commission_line = self.env['commission.lines']
            sales_commission_line = commission_line.create({
                'date': fields.Date.today(),
                'description': add_discription,
                'user_id': self.user_id.id,
                'invoice_reference': self.name,
                'commission_name': sales_commission.name,
                'commission_type': sales_commission.commission_type,
                'partner_id': self.partner_id.id,
                'commission_amount': amount

            })
            if self.user_id.partner_id:
                self.user_id.partner_id.commission_counter += amount
            return sales_commission_line


class SalesInvoiceLine(models.Model):
    _name = 'sales.commission.invoice.line'
    _description = 'sales commission invoice line'

    date = fields.Date()
    description = fields.Text()
    name = fields.Char()
    commission_type = fields.Selection([
        ('standard', 'Standard'),
        ('partner', 'Partner Based'),
        ('product/category', 'Product/Category')
    ])
    user_id = fields.Many2one('res.users', string="Sales Person")
    currency_id = fields.Many2one(related='sales_invoice_id.currency_id', store=True, string='Currency', readonly=True)
    commission_amount = fields.Monetary(readonly=True)
    sales_invoice_id = fields.Many2one('account.move')

