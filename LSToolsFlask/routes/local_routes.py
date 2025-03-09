from flask import jsonify

from routes import api
from services import local_service
from response_base import response
from flask_restx import Resource

ns_local = api.namespace('Local', description='Local operations')


@ns_local.route('/open_language_dir')
class OpenLanguageDir(Resource):
    @ns_local.doc(description='打开 studio language 文件夹')
    def get(self):
        response.start()
        res = local_service.open_language_dir()
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)
