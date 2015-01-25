__author__ = 'mildronize'

from pyramid.view import view_config

from r2als import models
from r2als.libs.solutions import InitialSolution
from r2als.libs.exports import ExportJson, ExportJointjs
from r2als.libs import next_solution_methods

@view_config(route_name='solution_generator', renderer='/solution_generator/index.mako')
def index(request):
    return dict()

@view_config(route_name='solution_generator.initial', renderer='/solution_generator/index.mako')
def index_initial(request):
    return dict()

# @view_config(route_name='apis.solution_generator',renderer='json')
# def solution_generator_api_json(request):
#
#     member = models.Member.objects(member_id = '5710110997').first()
#     if member is None:
#         print('Not found the member')
#         exit()
#
#     solution = InitialSolution(member).start()
#     # mSemesters = next_solution_methods.MoveWholeChain(solution).start()
#
#     json_obj = ExportJson(member, mSemesters).get()
#     return ExportJointjs(json_obj).get()

@view_config(route_name='apis.solution_generator.initial',renderer='json')
def solution_generator_api_initial(request):

    member = models.Member.objects(member_id = '5710110997').first()
    if member is None:
        print('Not found the member')
        exit()

    solution = InitialSolution(member).start()
    # mSemesters = next_solution_methods.MoveWholeChain(solution).start()
    json_obj = ExportJson(member, solution['semesters']).get()
    return ExportJointjs(json_obj).get()
