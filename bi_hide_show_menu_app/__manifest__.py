# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "All in one Hide Menu,Submenu, Field and Reports",
    "version" : "13.0.0.1",
    "category" : "Extra Tools",
    "depends" : ['base'],
    "author": "BrowseInfo",
    "summary": 'Hide menu hide report hide submenu hide field hide any menu hide any report hide any submenu hide any field hide all hide all in one menu hide user wise hide menu user wise hide report user wise invisible menu invisible report user wise report access hides',
    "description": """
        Hide any menu, sub menu, fields, report for any users and groups
    """ , 
    "website" : "https://www.browseinfo.in",
    "price": 9,
    "currency": 'EUR',
    "data": [
        'security/ir.model.access.csv',
        'views/res_user.xml',
        'views/res_group.xml',
        'views/ir_actions_report.xml',
        'views/view_ir_model_fields.xml',     
    ],
    'qweb': [
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url" : 'https://youtu.be/tQkfGvcpXpQ',
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
