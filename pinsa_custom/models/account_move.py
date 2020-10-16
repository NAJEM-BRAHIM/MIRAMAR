# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    qty_box = fields.Integer('Number of Box')
    virtual_box = fields.Boolean(related='product_id.can_be_virtual')
