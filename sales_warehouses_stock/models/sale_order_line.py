# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from collections import defaultdict
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_per_warehouse_ids = fields.One2many('warehouse.stock.qty', 'sale_order_line_id', readonly=True)

    @api.depends('product_id', 'customer_lead', 'product_uom_qty', 'order_id.warehouse_id', 'order_id.commitment_date')
    def _compute_qty_at_date(self):
        """ Compute the quantity forecasted of product at delivery date. There are
        two cases:
         1. The quotation has a commitment_date, we take it as delivery date
         2. The quotation hasn't commitment_date, we compute the estimated delivery
            date based on lead time"""
        qty_processed_per_product = defaultdict(lambda: 0)
        grouped_lines = defaultdict(lambda: self.env['sale.order.line'])
        # We first loop over the SO lines to group them by warehouse and schedule
        # date in order to batch the read of the quantities computed field.
        for line in self:
            if not line.display_qty_widget:
                continue
            line.qty_per_warehouse_ids = False
            line.warehouse_id = line.order_id.warehouse_id
            warehouse_ids = line.warehouse_id
            warehouse_ids += self.env['stock.warehouse'].search([('company_id', '=', line.order_id.company_id.id), ('id', '!=', line.warehouse_id.id)])
            for warehouse_id in warehouse_ids:
                if line.order_id.commitment_date:
                    date = line.order_id.commitment_date
                else:
                    confirm_date = line.order_id.date_order if line.order_id.state in ['sale', 'done'] else datetime.now()
                    date = confirm_date + timedelta(days=line.customer_lead or 0.0)
                grouped_lines[(warehouse_id.id, date)] |= line

        treated = self.browse()
        for (warehouse, scheduled_date), lines in grouped_lines.items():
            product_qties = lines.mapped('product_id').with_context(to_date=scheduled_date, warehouse=warehouse).read([
                'qty_available',
                'free_qty',
                'virtual_available',
            ])
            qties_per_product = {
                (product['id'], warehouse): (product['qty_available'], product['free_qty'], product['virtual_available'])
                for product in product_qties
            }
            for line in lines:
                if line.warehouse_id.id == warehouse:
                    line.scheduled_date = scheduled_date
                    qty_available_today, free_qty_today, virtual_available_at_date = qties_per_product[(line.product_id.id, warehouse)]
                    line.qty_available_today = qty_available_today - qty_processed_per_product[(line.product_id.id, warehouse)]
                    line.free_qty_today = free_qty_today - qty_processed_per_product[(line.product_id.id, warehouse)]
                    line.virtual_available_at_date = virtual_available_at_date - qty_processed_per_product[(line.product_id.id, warehouse)]
                    qty_processed_per_product[(line.product_id.id, warehouse)] += line.product_uom_qty
                    self.env['warehouse.stock.qty'].create({
                        'sale_order_line_id': line.id,
                        'warehouse_id': warehouse,
                        'qty_available': line.qty_available_today,
                        'free_qty': line.free_qty_today,
                        'virtual_available': line.virtual_available_at_date
                    })
                else:
                    qty_available_today_var, free_qty_today_var, virtual_available_at_date_var = qties_per_product[(line.product_id.id, warehouse)]
                    qty_available_today = qty_available_today_var - qty_processed_per_product[(line.product_id.id, warehouse)]
                    free_qty_today = free_qty_today_var - qty_processed_per_product[(line.product_id.id, warehouse)]
                    virtual_available_at_date = virtual_available_at_date_var - qty_processed_per_product[(line.product_id.id, warehouse)]
                    qty_processed_per_product[(line.product_id.id, warehouse)] += line.product_uom_qty
                    self.env['warehouse.stock.qty'].create({
                        'sale_order_line_id': line.id,
                        'warehouse_id': warehouse,
                        'qty_available': qty_available_today,
                        'free_qty': free_qty_today,
                        'virtual_available': virtual_available_at_date
                    })

            treated |= lines
        remaining = (self - treated)
        remaining.virtual_available_at_date = False
        remaining.scheduled_date = False
        remaining.free_qty_today = False
        remaining.qty_available_today = False
        remaining.warehouse_id = False