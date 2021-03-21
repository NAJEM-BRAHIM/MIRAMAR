# -*- coding: utf-8 -*-
# from odoo import http


# class RtInsurance(http.Controller):
#     @http.route('/rt_insurance/rt_insurance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rt_insurance/rt_insurance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rt_insurance.listing', {
#             'root': '/rt_insurance/rt_insurance',
#             'objects': http.request.env['rt_insurance.rt_insurance'].search([]),
#         })

#     @http.route('/rt_insurance/rt_insurance/objects/<model("rt_insurance.rt_insurance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rt_insurance.object', {
#             'object': obj
#         })
