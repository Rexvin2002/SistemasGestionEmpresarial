# -*- coding: utf-8 -*-
# from odoo import http


# class GestionZoo(http.Controller):
#     @http.route('/gestion_zoo/gestion_zoo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_zoo/gestion_zoo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_zoo.listing', {
#             'root': '/gestion_zoo/gestion_zoo',
#             'objects': http.request.env['gestion_zoo.gestion_zoo'].search([]),
#         })

#     @http.route('/gestion_zoo/gestion_zoo/objects/<model("gestion_zoo.gestion_zoo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_zoo.object', {
#             'object': obj
#         })

