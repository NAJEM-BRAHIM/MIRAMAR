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

class resConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sale_order_line_record_limit = fields.Integer(string="Record Limit", default=10, config_parameter='sale_order_line_record_limit')
    sale_order_status  = fields.Selection([('sale','Confirm order'),('done','Done (Locked)'),('both','Both')],string="Price History Based On", default="sale", config_parameter='sale_order_status')
    purchase_order_line_record_limit = fields.Integer(string="Record Limit", default=10, config_parameter='purchase_order_line_record_limit')
    purchase_order_status = fields.Selection([('purchase','Purchase order'),('done','Done (Locked)'),('both','Both')],string="Price History Based On", default="purchase", config_parameter='purchase_order_status')
    
    
    def get_values(self):
        res = super(resConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        sale_order_line_record_limit = ICPSudo.get_param('sale_order_line_record_limit')
        sale_order_status = ICPSudo.get_param('sale_order_status')
        purchase_order_line_record_limit = ICPSudo.get_param('purchase_order_line_record_limit')
        purchase_order_status = ICPSudo.get_param('purchase_order_status')
        res.update(
            sale_order_line_record_limit=int(sale_order_line_record_limit),
            sale_order_status=sale_order_status,
            purchase_order_line_record_limit = int(purchase_order_line_record_limit),
            purchase_order_status = purchase_order_status
        )
        return res


