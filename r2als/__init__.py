
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings

from r2als import config
from r2als import models
from r2als.routes import add_routes


def main(global_config, **settings):

    r2als_session_factory = session_factory_from_settings(settings)

    pyramid_config = Configurator(settings=settings,
                                  session_factory=r2als_session_factory)

    app_configuration = config.Configurator(config.root_path + 'development.ini')
    app_configuration.set('mongodb.is_drop_database', False)
    models.initial(app_configuration.settings)

    add_routes(pyramid_config)
    pyramid_config.scan('r2als.views')

    return pyramid_config.make_wsgi_app()
