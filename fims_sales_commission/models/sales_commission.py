# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import fields, api, models, exceptions

class SalesCommission(models.Model):
    _name = 'sales.commission'
    _description = "sales commission"

    name = fields.Char(string="Commission Name")
    commission_type = fields.Selection([
        ('standard', 'Standard Commission'),
        ('partner', 'Partner Based Commission'),
        ('product/category', 'Product/Category Commission')
    ])
    standard_commission_percentage = fields.Float(string="Standard Commission Percentage %")
    user_id = fields.Many2many('res.users', string="Sales Person")
    affiliated_partner_commission = fields.Float(string="Affiliated Partner Commission %")
    non_affiliated_partner_commission = fields.Float(string="Non-Affiliated Partner Commission %")
    product_category_lines = fields.One2many('sales.commission.line', 'sales_commission_id')

    @api.constrains('standard_commission_percentage', 'affiliated_partner_commission', 'non_affiliated_partner_commission')
    def _check_valid_percentage(self):
        for r in self:
            if (r.standard_commission_percentage or r.affiliated_partner_commission or r.non_affiliated_partner_commission) > 100:
                raise exceptions.ValidationError("A percentage can't greater than 100")


class SalesCommissionLine(models.Model):
    _name = 'sales.commission.line'
    _description = 'sales commission line'

    based_on = fields.Selection([
        ('product', 'Product'),
        ('category', 'Product Category')
    ])
    product_id = fields.Many2one('product.product')
    category_id = fields.Many2one('product.category')
    with_commission = fields.Selection([
        ('fix price', 'Fix Price'),
        ('commission percentage', 'Commission Percentage')
    ])
    target_price = fields.Float()
    above_price_commission = fields.Float(string="Above Price Commission %")
    commission = fields.Float(string="Commission %")
    sales_commission_id = fields.Many2one('sales.commission')

    @api.constrains('above_price_commission', 'commission')
    def _check_valid_percentage(self):
        for i in self:
            if (i.above_price_commission or i.commission) > 100:
                raise exceptions.ValidationError("A percentage can't greater than 100")

