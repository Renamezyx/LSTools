import time

from flask import jsonify, request
from flask_restx import Resource, fields, reqparse
from response_base import response
from routes import api
from services.users_service import UsersService

ns_users = api.namespace('users', description='Users operations')

users_model = api.model('UsersModel', {
    'id': fields.Integer(description="id"),
    'headers': fields.String(description="headers"),
    'username': fields.String(description="username"),
    'phone': fields.String(description="phone"),
})


@ns_users.route("/insert")
class UsersInsert(Resource):
    @api.expect(users_model)
    def post(self):
        response.start()
        data = request.json
        headers = data.get("headers", None)
        username = data.get("username", None)
        phone = data.get("phone", None)
        res = UsersService.users_insert(headers=headers, username=username, phone=phone)
        response.code = -1
        response.data = None
        if res == -1:
            response.message = "参数不合法"
        elif res == -2:
            response.message = "phone 重复"
        else:
            response.code = 0
            response.message = "success"
            response.data = res
        return jsonify(response.run_speed)


@ns_users.route("/update")
class UsersUpdate(Resource):
    @api.expect(users_model)
    def post(self):
        response.start()
        data = request.json
        headers = data.get("headers", None)
        username = data.get("username", None)
        phone = data.get("phone", None)
        id = data.get("id", None)
        res = UsersService.users_update(headers=headers, username=username, phone=phone, id=id)
        if res == -1:
            response.code = -1
            response.message = "参数不合法"
            response.data = None
        elif res == -2:
            response.message = "phone 重复"
        else:
            response.code = 0
            response.message = "success"
            response.data = res
        return jsonify(response.run_speed)


@ns_users.route("/delete")
class UsersDelete(Resource):
    @api.expect(users_model)
    def post(self):
        response.start()
        data = request.json
        id = data.get("id", None)
        res = UsersService.users_delete(id=id)
        if res == -1:
            response.code = -1
            response.message = "参数不合法"
            response.data = None
        else:
            response.code = 0
            response.message = "success"
            response.data = res
        return jsonify(response.run_speed)


parser = reqparse.RequestParser()
parser.add_argument('phone', type=str, required=False, help="手机号")


@ns_users.route("/select")
class UserSelect(Resource):
    @api.expect(parser)
    def get(self):
        response.start()
        args = parser.parse_args()
        phone = args.get("phone", None)
        res = UsersService.users_select(phone=phone, script_name="push_script")
        response.code = 0
        response.data = res
        response.message = "success"
        return jsonify(response.run_speed)
