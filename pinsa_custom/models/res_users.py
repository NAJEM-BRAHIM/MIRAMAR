# -*- coding: utf-8 -*-

from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    categ_ids = fields.Many2many('product.category')
