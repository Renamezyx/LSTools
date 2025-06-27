from flask import jsonify
from flask_restx import Resource, reqparse

from response_base import response
from routes import api
from services import proxy_service

ns_proxy = api.namespace('Proxy', description='Proxy operations')
parser = reqparse.RequestParser()
parser.add_argument('timeout', type=int, required=True)


@ns_proxy.route("/get_battle_headers")
class GetBattleHeaders(Resource):
    @ns_proxy.param('timeout', '超时时间（秒）', required=True)
    def get(self):
        response.start()
        args = parser.parse_args()
        timeout = args['timeout']
        res = proxy_service.get_battle_headers(sleep_time=int(timeout))
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)


@ns_proxy.route("/get_game_studio_setting")
class GetGameStudioSetting(Resource):
    @ns_proxy.param('timeout', '超时时间（秒）', required=True)
    def get(self):
        response.start()
        args = parser.parse_args()
        timeout = args['timeout']
        res = proxy_service.get_game_studio_setting(sleep_time=int(timeout))
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)
