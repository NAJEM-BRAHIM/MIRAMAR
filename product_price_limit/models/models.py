# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("price_unit")
    def _onchange_total_amount(self):
        for rec in self:
            if not rec.user_has_groups('account.group_account_manager'):
                inc_price = 0.0
                dec_price = 0.0
                inc_price = rec.product_id.lst_price + rec.product_id.lst_price * .03
                dec_price = rec.product_id.lst_price - rec.product_id.lst_price * .03
                if inc_price >= rec.product_id.lst_price and rec.price_unit >= inc_price:
                    rec.price_unit = inc_price
                elif dec_price <= rec.product_id.lst_price and rec.price_unit <= dec_price:
                    rec.price_unit = dec_price
                else:
                    rec.price_unit


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    @api.onchange("fixed_price")
    def _onchange_total_amount(self):
        for rec in self:
            if not rec.user_has_groups('account.group_account_manager'):
                inc_price = 0.0
                dec_price = 0.0
                inc_price = rec.product_tmpl_id.lst_price + rec.product_tmpl_id.lst_price * .03
                dec_price = rec.product_tmpl_id.lst_price - rec.product_tmpl_id.lst_price * .03
                if inc_price >= rec.product_tmpl_id.lst_price and rec.fixed_price >= inc_price:
                    rec.fixed_price = inc_price
                elif dec_price <= rec.product_tmpl_id.lst_price and rec.fixed_price <= dec_price:
                    rec.fixed_price = dec_price
                else:
                    rec.fixed_price


class ProductTemplate(models.Model):
    _inherit = "product.template"

    price = fields.Float(compute='_compute_total')

    def _compute_total(self):
        for rec in self:
            rec.price = rec.list_price

    @api.onchange("list_price")
    def _onchange_total_amount(self):
        for rec in self:
            if not rec.user_has_groups('account.group_account_manager'):
                inc_price = 0.0
                dec_price = 0.0
                inc_price = rec.price + rec.price * .03
                dec_price = rec.price - rec.price * .03
                if inc_price >= rec.price and rec.list_price >= inc_price:
                    rec.list_price = inc_price
                elif dec_price <= rec.price and rec.list_price <= dec_price:
                    rec.list_price = dec_price
                else:
                    rec.list_price
