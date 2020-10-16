# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_box = fields.Integer('Number of Box', readonly=False)
    virtual_box = fields.Boolean(related='product_id.can_be_virtual')
