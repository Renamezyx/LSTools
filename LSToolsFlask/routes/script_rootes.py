from flask import jsonify
from flask_restx import Resource, fields, reqparse
from services.script_service import ScriptService
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


script_start_model = api.model('ScriptModel', {
    'script_name': fields.String(required=True, description="脚本名称"),
    'script_params': fields.List(fields.String, description="脚本参数 string")
})


@ns_script.route("/script/start")
class ScriptStart(Resource):
    @api.expect(script_start_model)
    def post(self):
        response.start()
        from flask import request
        req_data = request.get_json()
        script_name = req_data.get("script_name")
        script_params = req_data.get("script_params", [])
        res = ScriptService.script_start(script_name, script_params)
        response.code = 0
        response.data = res
        response.message = "success"
        return jsonify(response.run_speed)


script_stop_parser = reqparse.RequestParser()
script_stop_parser.add_argument('pid', type=int, help="进程pid")
script_stop_parser.add_argument('script_name', type=str, help="脚本名称")


@ns_script.route("/script/stop")
class ScriptStop(Resource):
    @api.expect(script_stop_parser)
    def get(self):
        response.start()
        args = script_stop_parser.parse_args()
        pid = args.get("pid", None)
        script_name = args.get("script_name", "")
        response.code = 0
        response.data = ScriptService.script_stop(pid=pid, script_name=script_name)
        response.message = "success"
        return jsonify(response.run_speed)
