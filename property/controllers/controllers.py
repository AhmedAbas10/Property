# -*- coding: utf-8 -*-
from odoo import http


class TestApi(http.Controller):

    @http.route('/api/test', methods=["GET"] , type="http" , auth="none" , csrf=False)
    def tset_end_point(self, **kw):
        return "Hello, world"

    # @http.route('/priority/priority/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('priority.listing', {
    #         'root': '/priority/priority',
    #         'objects': http.request.env['priority.priority'].search([]),
    #     })
    #
    # @http.route('/priority/priority/objects/<model("priority.priority"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('priority.object', {
    #         'object': obj
    #     })

