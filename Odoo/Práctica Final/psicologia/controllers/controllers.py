# -*- coding: utf-8 -*-
# from odoo import http


# class Psicologia(http.Controller):
#     @http.route('/psicologia/psicologia', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/psicologia/psicologia/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('psicologia.listing', {
#             'root': '/psicologia/psicologia',
#             'objects': http.request.env['psicologia.psicologia'].search([]),
#         })

#     @http.route('/psicologia/psicologia/objects/<model("psicologia.psicologia"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('psicologia.object', {
#             'object': obj
#         })

