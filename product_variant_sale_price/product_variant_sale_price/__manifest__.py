# -*- coding: utf-8 -*-

{
    'name': 'Product Variant Sale Price',
    'summary': 'Allows to write fixed prices in product variants',
    'version': '12.0.1.0.0',
    'category': 'Product Management',
    'website': 'https://odoo-community.org/',
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'views/product_views.xml',
    ],
}
