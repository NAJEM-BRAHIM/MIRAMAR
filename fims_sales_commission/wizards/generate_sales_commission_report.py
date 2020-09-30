# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import models, fields, api

class CommissionLineCreateReport(models.Model):
    _name = 'commission.line.create.report'
    _description = 'commission line create report'

    user_id = fields.Many2one('res.users', string='Sales Person', required=True, default=lambda self:self.env.uid)
    from_date = fields.Date(required=True, default=fields.Date.today)
    to_date = fields.Date(required=True, default=fields.Date.today)

    def print_report(self):
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        return self.env.ref('fims_sales_commission.fims_sales_commission_report_action').report_action(self, data=data)