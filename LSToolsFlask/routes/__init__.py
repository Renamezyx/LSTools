from flask_restx import Api

api = Api(version="1.0", title="LSTools", description="")
from .local_routes import ns_local
from .request_routes import ns_request
from .file_routes import ns_file
from .preformance_routes import ns_performance
from .script_rootes import ns_script
from .stream_routes import ns_stream
from .users_routes import ns_users
from .proxy_routes import ns_proxy
api.add_namespace(ns_local)
api.add_namespace(ns_proxy)
api.add_namespace(ns_request)
api.add_namespace(ns_file)
api.add_namespace(ns_performance)
api.add_namespace(ns_script)
api.add_namespace(ns_stream)
api.add_namespace(ns_users)
