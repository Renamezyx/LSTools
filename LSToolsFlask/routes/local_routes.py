from flask import jsonify

from routes import api
from services import local_service
from response_base import response
from flask_restx import Resource

ns_test = api.namespace('Test', description='Test operations')
ns_local = api.namespace('Local', description='Local operations')


@ns_test.route('/test')
class Test(Resource):
    @ns_test.doc(description='这是一个测试接口')
    def get(self):
        return "hello"


@ns_local.route('/open_log_dir')
class OpenLogsDir(Resource):
    @ns_local.doc(description='打开 studio logs 文件夹')
    def get(self):
        response.start()
        res = local_service.open_logs_dir()
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)


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


@ns_local.route('/switch_branch')
class SwitchBranch(Resource):
    @ns_local.doc(description='切换 studio 分支')
    def get(self):
        response.start()
        res = local_service.switch_branch()
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)


@ns_local.route('/update_effects')
class UpdateEffects(Resource):
    @ns_local.doc(description='清除本地美颜缓存')
    def get(self):
        response.start()
        res = local_service.update_effects()
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)


@ns_local.route('/clear_screen')
class ClearScreen(Resource):
    @ns_local.doc(description='清除本地场景')
    def get(self):
        response.start()
        res = local_service.clear_screen()
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)


@ns_local.route('/generate_finsh_pk')
class GenerateFinshPK(Resource):
    @ns_local.doc(description='生成完成PK参数')
    def get(self):
        response.start()
        res = local_service.generate_finsh_pk()
        response.code = 0
        response.data = {}
        response.message = res if res is not None else ''
        return jsonify(response.run_speed)

# routes = [
#     ('/test', Test),
#     ('/open_log_dir', OpenLogsDir),
#     ('/open_language_dir', OpenLanguageDir),
#     ('/switch_branch', SwitchBranch),
#     ('/update_effects', UpdateEffects),
#     ('/clear_screen', ClearScreen),
#     ('/generate_finsh_pk', GenerateFinshPK),
# ]
# # 循环添加路由和对应的资源类
# for route, resource_class in routes:
#     api.add_resource(resource_class, route)
