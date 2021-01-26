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

{
    'name': "Sales and Purchase Price History for Products",
    'version': "13.0.0.0",
    'summary': "With the help of this module, You can find the rate which you have given to that customers/suppliers in past for that product.",
    'category': 'Sales',
    'description': """
    purchase price history
    sale price history
    easy to find previous cost price
    easy to find previous sale price
    price history
    purchase cost history
    inherit product
    track the price in product template
    track the price in product variant
    product wise sale price history
    product wise purchase price history
    product wise sale history
    
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base', 'sale_management', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_product.xml',
        'views/inherited_res_config_setting.xml',
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/VGs7aaPtW9s',
    'images': ['static/description/banner.png'],
    "price": 0,
    "currency": 'EUR',
    
}
