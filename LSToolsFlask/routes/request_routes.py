import requests
from flask import jsonify
from flask_restx import Resource

from response_base import response
from routes import api
from services import request_service

ns_request = api.namespace('Request', description='Request operations')


@ns_request.route("/finish_battle")
class Finish_Battle(Resource):
    def get(self):
        response.start()
        res = request_service.finish_pk()
        response.code = 0
        response.data = {}
        if isinstance(res, requests.models.Response) and res.status_code == 200:
            response.message = res.json()
        else:
            response.message = res
        return jsonify(response.run_speed)
