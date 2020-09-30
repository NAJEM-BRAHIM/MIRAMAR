# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_commission_ids = fields.One2many('sales.commission.info', 'sale_id', readonly=True)

    def action_confirm(self):
        confirm = super(SaleOrder, self).action_confirm()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        if get_param('fims_sales_commission.commission_based_on') == 'saleorder':
            self.generate_sales_commission()

        return confirm

    def action_cancel(self):
        state = super(SaleOrder, self).action_cancel()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        if get_param('fims_sales_commission.commission_based_on') == 'saleorder':
            self.generate_sales_commission()
        return state


    def calculate_commission(self,amount,discount):
        return (amount * discount)/100


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
                    for so_line in self.order_line:
                        if so_line.product_id == line.product_id:
                            if line.product_id.categ_id in get_category_ids:
                                pass
                            else:
                                if line.with_commission == 'fix price':
                                    if so_line.price_subtotal > line.target_price:
                                        commission = self.calculate_commission(so_line.price_subtotal,
                                                                               line.above_price_commission)
                                        percentage = line.above_price_commission
                                        description = line.product_id.name
                                        self.confirm_sales_commission(commission, sales_commission, percentage, description)
                                else:
                                    commission = self.calculate_commission(so_line.price_subtotal,
                                                                           line.commission)
                                    percentage = line.commission
                                    description = line.product_id.name
                                    self.confirm_sales_commission(commission, sales_commission, percentage, description)
                else:
                    for so_line in self.order_line:
                        if so_line.product_id.categ_id == line.category_id:
                            if line.with_commission == 'fix price':
                                if so_line.price_subtotal > line.target_price:
                                    commission = self.calculate_commission(so_line.price_subtotal,
                                                                           line.above_price_commission)
                                    percentage = line.above_price_commission
                                    description = line.category_id.name
                                    self.confirm_sales_commission(commission, sales_commission, percentage, description)
                            else:
                                commission = self.calculate_commission(so_line.price_subtotal,
                                                                       line.commission)
                                percentage = line.commission
                                description = line.category_id.name
                                self.confirm_sales_commission(commission, sales_commission, percentage, description)


    def confirm_sales_commission(self, commission, sales_commission, percentage, description):
        if commission:
            if self.state == 'cancel':
                amount = -(commission)
                add_discription = 'sale order cancel'
            else:
                amount = commission
                add_discription = sales_commission.commission_type + ' "' +sales_commission.name + '"' + " ( "+ str(percentage) +"%" + ") " +str(description)
            self.write({'sales_commission_ids': [(0, 0, {'date': fields.Date.today(),
                                                         'description': add_discription,
                                                         'name': sales_commission.name,
                                                         'commission_type': sales_commission.commission_type,
                                                         'user_id': self.user_id.id,
                                                         'commission_amount': amount
                                                         })]})
            commission_line = self.env['commission.lines']
            sales_commission_line = commission_line.create({
                'date': fields.Date.today(),
                'description': add_discription,
                'user_id': self.user_id.id,
                'order_reference': self.name,
                'sale_commission': amount,
                'commission_name': sales_commission.name,
                'commission_type': sales_commission.commission_type,
                'partner_id': self.partner_id.id,
                'commission_amount': amount

            })
            if self.user_id.partner_id:
                self.user_id.partner_id.commission_counter += amount
            return sales_commission_line



class SalesCommissionLine(models.Model):
    _name = 'sales.commission.info'
    _description = 'sales commission info'

    date = fields.Date()
    description = fields.Text()
    name = fields.Char()
    commission_type = fields.Selection([
        ('standard', 'Standard'),
        ('partner', 'Partner Based'),
        ('product/category', 'Product/Category')
    ])
    user_id = fields.Many2one('res.users', string="Sales Person")
    currency_id = fields.Many2one(related='sale_id.currency_id', store=True, string='Currency', readonly=True)
    commission_amount = fields.Monetary(readonly=True)
    sale_id = fields.Many2one('sale.order')
