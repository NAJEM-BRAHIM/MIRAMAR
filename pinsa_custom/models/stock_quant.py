# -*- coding: utf-8 -*-

from psycopg2 import OperationalError, Error
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    qty_box = fields.Float('Box Qty')

    def write(self, vals):
        """ Override to handle the "inventory mode" and create the inventory move. """
        if 'qty_box' or 'lot_id' in vals:
            self = self.sudo()
        return super(StockQuant, self).write(vals)

    @api.onchange('location_id', 'product_id', 'package_id', 'owner_id', 'qty_box')
    def _onchange_location_or_product_id(self):
        vals = {}

        # Once the new line is complete, fetch the new theoretical values.
        if self.product_id and self.location_id:
            # Sanity check if a lot has been set.
            if self.lot_id:
                if self.tracking == 'none' or self.product_id != self.lot_id.product_id:
                    vals['lot_id'] = None
            quants = self._gather(self.product_id, self.location_id, lot_id=self.lot_id, package_id=self.package_id, owner_id=self.owner_id, strict=True)
            reserved_quantity = sum(quants.mapped('reserved_quantity'))
            quantity = sum(quants.mapped('quantity'))
            vals['reserved_quantity'] = reserved_quantity
            vals['qty_box'] = self.qty_box
            # Update `quantity` only if the user manually updated `inventory_quantity`.
            if float_compare(self.quantity, self.inventory_quantity, precision_rounding=self.product_uom_id.rounding) == 0:
                vals['quantity'] = quantity
            # Special case: directly set the quantity to one for serial numbers,
            # it'll trigger `inventory_quantity` compute.
            if self.lot_id and self.tracking == 'serial':
                vals['quantity'] = 1
        if vals:
            self.update(vals)

    @api.model
    def create(self, vals):
        res = super(StockQuant, self).create(vals)
        if 'qty_box' in vals:
            product = self.env['product.product'].browse(vals['product_id'])
            location = self.env['stock.location'].browse(vals['location_id'])
            lot_id = self.env['stock.production.lot'].browse(vals.get('lot_id'))
            package_id = self.env['stock.quant.package'].browse(vals.get('package_id'))
            owner_id = self.env['res.partner'].browse(vals.get('owner_id'))
            quant = self._gather(product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)
            if quant:
                quant = quant[0]
            else:
                quant = self.sudo().create(vals)
            # Set the `inventory_quantity` field to create the necessary move.
            quant.qty_box = self.qty_box
        return res

    @api.model
    def _get_inventory_fields_write(self):
        """ Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
        """
        return ['inventory_quantity', 'qty_box', 'lot_id']

    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        return ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id', 'inventory_quantity', 'qty_box']

    # Override the method
    @api.model
    def _update_available_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, in_date=None):
        """ Increase or decrease `reserved_quantity` of a set of quants for a given set of
        product_id/location_id/lot_id/package_id/owner_id.

        :param product_id:
        :param location_id:
        :param quantity:
        :param lot_id:
        :param package_id:
        :param owner_id:
        :param datetime in_date: Should only be passed when calls to this method are done in
                                 order to move a quant. When creating a tracked quant, the
                                 current datetime will be used.
        :return: tuple (available_quantity, in_date as a datetime)
        """
        self = self.sudo()
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)

        incoming_dates = [d for d in quants.mapped('in_date') if d]
        incoming_dates = [fields.Datetime.from_string(incoming_date) for incoming_date in incoming_dates]
        if in_date:
            incoming_dates += [in_date]
        # If multiple incoming dates are available for a given lot_id/package_id/owner_id, we
        # consider only the oldest one as being relevant.
        if incoming_dates:
            in_date = fields.Datetime.to_string(min(incoming_dates))
        else:
            in_date = fields.Datetime.now()
        for quant in quants:
            try:
                with self._cr.savepoint():
                    self._cr.execute("SELECT 1 FROM stock_quant WHERE id = %s FOR UPDATE NOWAIT", [quant.id], log_exceptions=False)
                    quant.write({
                        'quantity': quant.quantity + quantity,
                        'in_date': in_date,
                        # Customisation Start
                        # 'qty_box': quant.qty_box + self.env.context.get('pinsa_qty_box') if self.env.context.get('pinsa_qty_box') else 0.0
                        # Customisation End
                    })
                    break
            except OperationalError as e:
                if e.pgcode == '55P03':  # could not obtain the lock
                    continue
                else:
                    raise
        else:
            self.create({
                'product_id': product_id.id,
                'location_id': location_id.id,
                'quantity': quantity,
                'lot_id': lot_id and lot_id.id,
                'package_id': package_id and package_id.id,
                'owner_id': owner_id and owner_id.id,
                'in_date': in_date,
                # Customisation Start
                # 'qty_box': self.env.context.get('pinsa_qty_box')
                # Customisation End
            })
        return self._get_available_quantity(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=False, allow_negative=True), fields.Datetime.from_string(in_date)
