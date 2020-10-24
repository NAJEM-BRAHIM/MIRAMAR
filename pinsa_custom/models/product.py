# -*- coding: utf-8 -*-

from odoo import api,  fields, models,  SUPERUSER_ID


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    can_be_virtual = fields.Boolean(string="caja virtual")
    qty_box = fields.Float(string='Qty Box')

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        ''' Allow user to access the product which can be set on user'''
        if self.env.user.id != SUPERUSER_ID:
            for cat in self.env.user.categ_ids:
                args += ['|', ('categ_id', 'child_of', cat.id)]
            args += [('categ_id', 'in', [g.id for g in self.env.user.categ_ids])]
        return super(ProductTemplate, self).search(args, offset=0, limit=0, order=None, count=False)
