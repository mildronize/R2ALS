
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
# from pyramid.request import Request
# from pyramid.request import Response

from r2als import config
from r2als import models
from r2als.routes import add_routes

from r2als.libs.logs import Log

l = Log("__init__").getLogger()
#
# def request_factory(environ):
#     request = Request(environ)
#     if request.is_xhr:
#         request.response = Response()
#         request.response.headerlist = []
#         request.response.headerlist.extend(
#             (
#                 ('Access-Control-Allow-Origin', '*'),
#                 ('Content-Type', 'application/json')
#             )
#         )
#         l.info("pass")
#     else:
#         l.error("Nope")
#     l.info(request)
#     return request

def main(global_config, **settings):

    r2als_session_factory = session_factory_from_settings(settings)

    pyramid_config = Configurator(settings=settings,
                                  session_factory=r2als_session_factory
                                  )
    # request_factory=request_factory

    app_configuration = config.Configurator(config.root_path + 'development.ini')
    app_configuration.set('mongodb.is_drop_database', False)
    models.initial(app_configuration.settings)

    add_routes(pyramid_config)

    pyramid_config.scan('r2als.views')

    # WSGI for Cross Origin Resource Sharing (CORS)
    from wsgicors import CORS
    return CORS(pyramid_config.make_wsgi_app(), headers="*", methods="*", maxage="180", origin="*")
    # return pyramid_config.make_wsgi_app()
