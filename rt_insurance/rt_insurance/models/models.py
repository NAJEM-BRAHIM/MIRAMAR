# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    insurance_credit_limit = fields.Float(related="partner_id.insurance_credit_limit")
    vat = fields.Char(related="partner_id.vat")
