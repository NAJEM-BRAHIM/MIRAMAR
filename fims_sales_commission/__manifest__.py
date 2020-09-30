# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
{
    'name': 'Sales Commission',
    'category': 'Sale',
    'summary': 'This module will allow to manage sales commission',
    'version': '13.0.1',
    'license': 'OPL-1',
    'description': """This module will allow manage sales commision""",
    'author': 'Fortutech IMS Pvt. Ltd.',
    'website': 'https://www.fortutechims.com',
    'depends': ['sale_management','account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        'views/sales_commission.xml',
        'views/commission_line.xml',
        'views/res_partner.xml',
        'wizards/make_invoice_commission_lines.xml',
        'wizards/generate_sales_commission_report.xml',
        'views/res_config_settings.xml',
        'reports/sales_commission_report.xml',
    ],
    'price': 25,
    'currency': 'EUR',
    'installable': True,
    'application': True,
    'auto_install': False,
    'images':['static/description/banner.png'],
}
