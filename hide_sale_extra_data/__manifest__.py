# -*- coding: utf-8 -*-

{
    'name': "Hide Extra Data For DMS",
    'version': '1.0',
    'summary': 'Hide Extra Data For DMS Users Group.',
    'license': 'OPL-1',
    'author': "Kanak Infosystem LLP",
    'website': "https://kanakinfosystems.com",
    'category': 'Extra Tools',
    'depends': [
        'base', 'partner_risk_insurance',
        'sale', 'sale_margin', 'stock',
        'stock_account'
    ],
    'data': [
        'security/security.xml',
        'views/views.xml',
    ],
    'installable': True,
    'application': False,
}
