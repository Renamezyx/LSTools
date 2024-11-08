from flask import jsonify, request
from routes import api
from services import performance_service
from response_base import response
from flask_restx import Resource
from flask_restx import fields

ns_performance = api.namespace('Performance', description='Performance operations')

device_model = api.model('Device', {
    'device': fields.String(required=True, description='The device name')
})


@ns_performance.route("/get_conf")
class GetConf(Resource):
    @ns_performance.expect(device_model)
    @ns_performance.doc(description='获取配置文件')
    def post(self):
        response.start()
        data = request.json
        device = data.get('device') if data else None
        res = performance_service.get_conf(device)
        response.code = 0
        response.data = res if res is not None else ''
        response.message = {}
        return jsonify(response.run_speed)
