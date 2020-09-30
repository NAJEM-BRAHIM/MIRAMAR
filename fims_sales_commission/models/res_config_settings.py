# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import api, fields, models

class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_based_on = fields.Selection([
        ('saleorder', 'Commission Based On Sale Order'),
        ('invoice', 'Commission Based On Invoice')
    ])

    @api.model
    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            commission_based_on = ICPSudo.get_param('fims_sales_commission.commission_based_on', default='saleorder'),
        )
        return res


    def set_values(self):
        super(ResConfigSetting, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('fims_sales_commission.commission_based_on', self.commission_based_on)
