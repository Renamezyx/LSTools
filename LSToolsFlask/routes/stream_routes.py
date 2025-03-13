from flask import jsonify, request
from flask_restx import Resource, fields
from response_base import response
from routes import api

ns_stream = api.namespace('Stream', description='Stream operations')

stream_model = api.model('StreamModel', {
    'phone': fields.String(required=True, description="手机号"),
})


@ns_stream.route("/stream/push")
class StreamPush(Resource):
    @api.expect(stream_model)
    def post(self):
        response.start()
        data = request.json
        phone = data.get("phone", None)
        response.code = 0
        response.data = {"phone": phone}
        return jsonify(response.run_speed)


@ns_stream.route("/stream/finish")
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


@ns_stream.route("/stream/stats")
class StreamStats(Resource):
    def get(self):
        response.start()
        response.code = 0
        response.message = "success"
        return jsonify(response.run_speed)
