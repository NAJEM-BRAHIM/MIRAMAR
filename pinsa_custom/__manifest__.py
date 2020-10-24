# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
#################################################################################

{
    'name': 'Customization For Pinsa',
    'version': '1.0',
    'summary': '',
    'sequence': 30,
    'description': """
    """,
    'category': 'extra',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': ['product', 'account', 'stock', 'sale_stock', 'purchase'],
    'data': [
        'reports/sale_report_templates.xml',
        'reports/invoice_report_templates.xml',
        # 'reports/report_deliveryslip.xml',
        'views/account_move_views.xml',
        'views/res_users_views.xml',
        'views/sale_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml',
        'views/purchase_views.xml'
    ],
    'installable': True
}
