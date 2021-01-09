# -*- coding: utf-8 -*-
{
    'name': "(Sales) Show warehouses stock quantity",
    'summary': "Show warehouses stock quantity in the Quotations.",
    'description': "Show warehouses stock quantity in the Quotations.",
    'author': "Sayed Ahmed Abbas Ahmed",
    'category': 'Sales/Sales',
    'version': '1.0',
    'price': 0.00,
    'currency': 'USD',
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'depends': ['sale_management', 'sale_stock'],
    'qweb': ['static/src/xml/qty_at_date.xml'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
}