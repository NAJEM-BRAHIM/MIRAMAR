# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<http://kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <http://kanakinfosystems.com/license>
#################################################################################
{
    'name': 'Product Price Limit',
    'version': '1.0',
    'summary': 'An app which helps to limit product prices change.',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'http://www.kanakinfosystems.com',
    'depends': ['sale_management', 'product'],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
