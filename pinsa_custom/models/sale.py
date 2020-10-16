# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_box = fields.Integer('Number of Box')
    virtual_box = fields.Boolean(related='product_id.can_be_virtual')

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'qty_box': self.qty_box})
        return res
