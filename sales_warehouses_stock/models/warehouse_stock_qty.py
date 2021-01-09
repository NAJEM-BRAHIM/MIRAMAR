# -*- coding: utf-8 -*-

from odoo import models, fields


class WarehouseStockQty(models.Model):
    _name = 'warehouse.stock.qty'
    _description = 'Warehouse stock qty'
    _rec_name = 'warehouse_id'

    sale_order_line_id = fields.Many2one('sale.order.line')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    qty_available = fields.Float(required=True)
    free_qty = fields.Float(required=True)
    virtual_available = fields.Float(required=True)
