import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request
import json


def valid_response(data, status, pagination_info):
    response_body = {
        'data': data,
        'message': "OuFF A7"
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'Error': error,
    }
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):

    # @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    # def post_propetry(self, **kw):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     if not vals.get('name'):
    #         return request.make_json_response({
    #             "Message": "اكتب الاسم ي عرص"
    #         }, status=400)
    #     try:
    #         res = request.env['property.property'].sudo().create(vals)
    #         if res:
    #             return request.make_json_response({
    #                 "Message": "A7a Enta Gamed Niek"
    #             }, status=201)
    #     except Exception as Error:
    #         return request.make_json_response({
    #             "Message": Error
    #         }, status=400)

    @http.route('/v1/property', methods=["POST"], type="http", auth="none", csrf=False)
    def post_propetry(self, **kw):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                "Message": "اكتب الاسم ي عرص"
            }, status=400)
        try:
            # res = request.env['property.property'].sudo().create(vals)
            cr = request.env.cr
            columns = ' , '.join(vals.keys())
            values = ' , '.join([ '%s'] * len(vals))
            print(columns)
            print(values)
            query = f"""
            INSERT INTO property_property ({columns}) VALUES ({values}) returning id , name , bedrooms 
            """
            cr.execute(query , tuple(vals.values()))
            res = cr.fetchone()
            print(res)
            if res:
                return request.make_json_response({
                    "Message": "A7a Enta Gamed Niek",
                    "id" :res[0],
                    "name" :res[1],
                    "bedrooms" :res[2],
                }, status=201)
        except Exception as Error:
            return request.make_json_response({
                "Message": Error
            }, status=400)

    @http.route('/v1/property/json', methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property.property'].sudo().create(vals)
        if res:
            return {
                "Message": "A7a Enta Gamed Niek",
                "id": res.id,
                "name": res.name,
            }

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property = request.env['property.property'].sudo().search([('id', '=', property_id)])
            print(property)
            if not property:
                return request.make_json_response({
                    "Message": "ID NOT FOUND !"
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property.write(vals)
            return request.make_json_response({
                "Message": "A7a Enta Gamed Niek",
                "id": property.id,
                "name": property.name,
            }, status=200)
        except Exception as Error:
            return request.make_json_response({
                "Message": Error
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property = request.env['property.property'].sudo().search([('id', '=', property_id)])
            if not property:
                return request.make_json_response({
                    "Message": "ID NOT FOUND !"
                }, status=400)
            return valid_response({
                "Message": "A7a Enta Gamed Niek",
                "id": property.id,
                "name": property.name,
                "ref": property.ref,
                "description": property.description,
                "bedrooms": property.bedrooms,
            }, status=200)
        except Exception as Error:
            return invalid_response({
                "Message": Error
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property = request.env['property.property'].sudo().search([('id', '=', property_id)])
            if not property:
                return invalid_response({
                    "Message": "ID NOT FOUND !"
                }, status=400)
            property.unlink()
            return request.make_json_response({
                "Message": "يتم حذف ",

            }, status=200)
        except Exception as Error:
            return invalid_response({
                "Message": Error
            }, status=400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_properties(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domian = []
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                property_domian += [('state', '=', params.get('state')[0])]
            property_ids = request.env['property.property'].sudo().search(property_domian, offset=offset, limit=limit)
            property_count = request.env['property.property'].sudo().search_count(property_domian)
            if not property_ids:
                return request.make_json_response({
                    "Message": "NO IDs WERE FOUND !"
                }, status=400)
            return valid_response([{
                "Message": "A7a Enta Gamed Niek",
                "id": property.id,
                "name": property.name,
                "ref": property.ref,
                "description": property.description,
                "bedrooms": property.bedrooms,
            } for property in property_ids], pagination_info={
                'page': page if page else 1,
                'limit': limit if limit else 1,
                'Pages': math.ceil(page * limit) if limit else 1,
                'Count': property_count,
            }, status=200)
        except Exception as Error:
            return invalid_response({
                "Message": Error
            }, status=400)
