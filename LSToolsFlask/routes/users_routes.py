from flask import jsonify, request
from flask_restx import Resource, fields, reqparse
from response_base import response
from routes import api
from dao.dao_users import DaoUsers

ns_users = api.namespace('Users', description='Users operations')

users_model = api.model('UsersModel', {
    'headers': fields.String(description="headers"),
    'username': fields.String(description="username"),
    'phone': fields.String(description="phone"),
})


@ns_users.route("/users/insert")
class UsersInsert(Resource):
    @api.expect(users_model)
    def post(self):
        response.start()
        data = request.json
        headers = data.get("headers", None)
        username = data.get("username", None)
        phone = data.get("phone", None)
        if headers is None or phone is None:
            response.code = -1
            response.message = "参数不合法"
            return jsonify(response.run_speed)
        else:
            dao_users = DaoUsers()
            res = dao_users.insert((headers, username, phone))
            response.code = 0
            response.data = res
            response.message = "success"
            return jsonify(response.run_speed)


@ns_users.route("/users/update")
class UsersUpdate(Resource):
    @api.expect(users_model)
    def post(self):
        response.start()
        data = request.json
        headers = data.get("headers", None)
        username = data.get("username", None)
        phone = data.get("phone", None)
        if phone is None or (headers is None and username is None):
            response.code = -1
            response.data = ""
            response.message = "参数不合法"
            return jsonify(response.run_speed)
        else:
            dao_users = DaoUsers()
            res = dao_users.update(headers=headers, username=username, phone=phone)
            response.code = 0
            response.data = res
            response.message = "success"
            return jsonify(response.run_speed)


@ns_users.route("/users/delete")
class UsersDelete(Resource):
    @api.expect(users_model)
    def post(self):
        response.start()
        data = request.json
        phone = data.get("phone", None)
        if phone is None:
            response.code = -1
            response.message = "参数不合法"
            return jsonify(response.run_speed)
        else:
            dao_users = DaoUsers()
            res = dao_users.delete(phone=phone)
            response.code = 0
            response.data = res
            response.message = "success"
            return jsonify(response.run_speed)


parser = reqparse.RequestParser()
parser.add_argument('phone', type=str, required=False, help="手机号")


@ns_users.route("/users/select")
class StreamStats(Resource):
    @api.expect(parser)
    def get(self):
        response.start()
        args = parser.parse_args()
        phone = args.get("phone", None)
        dao_users = DaoUsers()
        res = dao_users.select(phone=phone)
        response.code = 0
        response.data = res
        response.message = "success"
        return jsonify(response.run_speed)
