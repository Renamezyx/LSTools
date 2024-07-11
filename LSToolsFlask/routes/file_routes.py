from flask import jsonify
from werkzeug.datastructures import FileStorage
from routes import api
from services import file_service
from response_base import response
from flask_restx import Resource, reqparse

ns_file = api.namespace('File', description='File operations')

# 设置请求解析器，用于处理文件上传
file_upload_parser = reqparse.RequestParser()
file_upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='File to upload')


@ns_file.route('/upload')
class FileRoutes(Resource):
    @ns_file.doc(description='')
    @ns_file.expect(file_upload_parser)
    def post(self):
        response.start()
        args = file_upload_parser.parse_args()
        uploaded_file = args['file']
        res = file_service.upload_file(uploaded_file)
        response.code = 0
        response.data = {}
        response.message = str(res) if res is not None else ''
        return jsonify(response.run_speed)
