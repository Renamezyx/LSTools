from flask import jsonify
from flask_restx import Resource

from response_base import response
from routes import api
from services import proxy_service

ns_proxy = api.namespace('Proxy', description='Proxy operations')


@ns_proxy.route("/get_battle_headers<timeout>")
class GetBattleHeaders(Resource):
    def get(self, timeout):
        response.start()
        res = proxy_service.get_battle_headers(sleep_time=int(timeout))
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)

