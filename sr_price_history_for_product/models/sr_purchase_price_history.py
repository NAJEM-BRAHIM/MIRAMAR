# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class srPurchasePriceHistory(models.Model):
    _name = 'sr.purchase.price.history'
    _description = 'Purchase Price History'

    name = fields.Many2one("purchase.order.line",string="Purchase Order Line")  
    partner_id = fields.Many2one("res.partner",string="Customer")
    user_id = fields.Many2one("res.users",string="Sales Person")
    product_tmpl_id = fields.Many2one("product.template",string="Template Id")
    variant_id = fields.Many2one("product.product",string="Product")
    purchase_order_id = fields.Many2one("purchase.order",string="Purchase Order")
    purchase_order_date = fields.Datetime(string="Purchase Order Date")
    product_uom_qty = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Price")
    currency_id = fields.Many2one("res.currency",string="Currency Id")
    total_price = fields.Monetary(string="Total")

