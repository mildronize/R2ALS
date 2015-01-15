'''

@author: mildronize

'''

def apis_include(config):
    config.add_route('apis.solution_generator', '/solution_generator/json')
    # config.add_route('apis.events.list', '/events')

def add_routes(config):
    config.add_route('index', '/')

    # add apis route
    config.include(apis_include, route_prefix='/apis')

    config.add_route('solution_generator', '/solution_generator')

    config.add_static_view('public', 'public')
    # config.add_static_view('public', 'public', cache_max_age=3600)
