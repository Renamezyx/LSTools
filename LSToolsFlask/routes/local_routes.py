import json
import os

from flask import jsonify, request

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


@ns_local.route('/get_file')
class GetFileContent(Resource):
    @ns_local.doc(description='获取指定文件内容', params={
        'file_path': '文件的绝对路径',
        'is_json': '是否按 JSON 格式解析（true/false）'
    })
    def get(self):
        response.start()
        file_path = request.args.get('file_path', None)
        is_json = request.args.get('is_json', 'false').lower() == 'true'
        if file_path is not None and os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    if not is_json:
                        content = f.read()
                    else:
                        content = "".join(f.readlines())
                        content = json.loads(content)
                response.data = content
                response.code = 200
            except Exception as e:
                response.data = str(e)
                response.code = 500
        else:
            response.data = ""
            response.code = -1
            response.message = "路径不存在"

        return jsonify(response.run_speed)