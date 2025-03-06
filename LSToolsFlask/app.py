from flask import Flask
from flask_cors import CORS
from routes import api
from routes.local_routes import ns_local
# from routes.proxy_routes import ns_proxy
from routes.request_routes import ns_request
from routes.file_routes import ns_file
from routes.preformance_routes import ns_performance


def create_app():
    app = Flask(__name__)
    api.add_namespace(ns_local)
    # api.add_namespace(ns_proxy)
    api.add_namespace(ns_request)
    api.add_namespace(ns_file)
    api.add_namespace(ns_performance)
    CORS(app)
    api.init_app(app)
    return app
