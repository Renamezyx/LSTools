from flask import jsonify, request, Response, stream_with_context
from flask_restx import Resource, fields
from response_base import response
from routes import api
from services.push_stream_service import PushStreamService

ns_stream = api.namespace('stream', description='Stream operations')

stream_model = api.model('StreamModel', {
    'phone': fields.String(required=True, description="手机号"),
})


@ns_stream.route("/push")
class StreamPush(Resource):
    @api.expect(stream_model)
    def post(self):
        response.start()
        data = request.json
        phone = data.get("phone", None)
        response.code = 0
        response.data = PushStreamService.push(phone)
        return jsonify(response.run_speed)


@ns_stream.route("/finish")
class StreamFinish(Resource):
    @api.expect(stream_model)
    def post(self):
        response.start()
        data = request.json
        phone = data.get("phone", None)
        response.code = 0
        response.data = {"phone": phone}
        response.message = "success"
        return jsonify(response.run_speed)


@ns_stream.route("/stats")
class StreamStats(Resource):
    def get(self):
        response.start()
        response.code = 0
        response.message = "success"
        return jsonify(response.run_speed)
