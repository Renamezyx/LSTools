from flask import jsonify
from flask_restx import Resource, fields, reqparse
from services.script_service import script_start
from response_base import response
from routes import api

ns_script = api.namespace('Script', description='Script operations')


@ns_script.route("/script/status")
class ScriptStatus(Resource):
    def get(self):
        response.start()
        res = "查询正在运行中的脚本"
        response.code = 0
        response.data = {}
        response.message = res
        return jsonify(response.run_speed)


script_model = api.model('ScriptModel', {
    'script_name': fields.String(required=True, description="脚本名称"),
    'script_params': fields.List(fields.String, description="脚本参数 string")
})


@ns_script.route("/script/start")
class ScriptStart(Resource):
    @api.expect(script_model)
    def post(self):
        response.start()
        from flask import request
        req_data = request.get_json()
        script_name = req_data.get("script_name")
        script_params = req_data.get("script_params", [])
        res = fr"执行脚本{script_name}, 参数{script_params}"
        res = script_start(script_name, script_params)
        response.code = 0
        response.data = {}
        response.message = res
        return jsonify(response.run_speed)


parser = reqparse.RequestParser()
parser.add_argument('pid', type=int, required=True, help="进程pid")


@ns_script.route("/script/end")
class ScriptEnd(Resource):
    @api.expect(parser)
    def get(self):
        response.start()
        args = parser.parse_args()
        pid = args.get("pid")
        res = f"结束进程{pid}"
        response.code = 0
        response.data = {}
        response.message = res
        return jsonify(response.run_speed)
