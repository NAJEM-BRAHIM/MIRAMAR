# -*- coding: utf-8 -*-
###############################################################################
#
#    Fortutech IMS Pvt. Ltd.
#    Copyright (C) 2016-TODAY Fortutech IMS Pvt. Ltd.(<http://www.fortutechims.com>).
#
###############################################################################
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    affiliated = fields.Boolean()
    commission_counter = fields.Monetary(store=True, readonly=True, string="Commission")

