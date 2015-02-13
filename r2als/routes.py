'''

@author: mildronize

'''

def apis_include(config):
    config.add_route('apis.solution_generator', '/solution_generator/')
    config.add_route('apis.solution_generator.initial', '/solution-generator/initial')

    config.add_route('apis.subjects', '/subjects')
    config.add_route('apis.subjects.search', '/subjects/search/{query_string}')
    config.add_route('apis.subject_groups.search', '/subject-groups/{subject_group}/search/{query_string}')

    config.add_route('apis.processor', '/processor')

def solution_generator_include(config):
    config.add_route('solution_generator', '/')
    config.add_route('solution_generator.initial','/initial')
    config.add_route('solution_generator.move_whole_chain','/move_whole_chain')

def add_routes(config):
    config.add_route('index', '/')

    # add apis route
    config.include(apis_include, route_prefix='/apis')

    config.include(solution_generator_include, route_prefix='/solution_generator')

    config.add_static_view('public', 'public')

    # config.add_static_view('public', 'public', cache_max_age=3600)
