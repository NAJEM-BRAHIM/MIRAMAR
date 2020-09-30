# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import models, _

class SalesCommisionReport(models.TransientModel):
    _name = "report.fims_sales_commission.sales_commission_doc"
    _description = 'create commission lines report'

    def _get_report_values(self, docids, data=None):
        form_data = data['form']
        domain = []
        if form_data.get('from_date') and form_data.get('to_date'):
            domain = [('date', '>=', form_data['from_date']), ('date', '<=', form_data['to_date'])]
        if form_data.get('user_id'):
            domain.append(('user_id', '=', form_data['user_id'][0]))
            domain.append(('invoice_id', '!=', False))
        docs = self.env['commission.lines'].search(domain)
        return {
            'doc_ids': self.ids,
            'doc_model': 'commission.lines',
            'docs': docs,
            'data': data,
        }
