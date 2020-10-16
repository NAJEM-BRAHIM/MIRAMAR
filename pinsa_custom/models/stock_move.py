# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_box = fields.Integer('Number of Box', compute='_compute_qty_box', readonly=False, store=True)
    virtual_box = fields.Boolean(related='product_id.can_be_virtual')

    @api.depends('purchase_line_id', 'sale_line_id')
    def _compute_qty_box(self):
        for move in self:
            # Incomming Order
            if move.picking_type_id.code == "incoming":
                move.qty_box = move.purchase_line_id.qty_box
            # Outgoing Order
            if move.picking_type_id.code == "outgoing":
                move.qty_box = move.sale_line_id.qty_box
