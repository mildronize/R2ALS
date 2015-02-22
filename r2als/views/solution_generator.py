__author__ = 'mildronize'

from pyramid.view import view_config
import copy
from r2als import models
from r2als.libs.solutions import InitialSolution
from r2als.libs.exports import ExportJson, ExportJointjs
from r2als.libs.logs import Log
from r2als.libs import next_solution_methods
from r2als.libs.next_solution_methods import *
from r2als.engines.validator import validator
from r2als.engines.tabu_manager import TabuManager


l = Log("view/solution_generator").getLogger()

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

    solution = InitialSolution(member).get_solution()
    validator(solution, ['*'])
    for i in range(10):
        l.info("-"*45)
        l.info("Random "+str(i) + " rounds ....")
        solution = RandomSubjectWithRules(solution).get_solution()
        solution = MoveWholeChain(solution).get_solution()
        solution.get_ready()
        if validator(solution, ['*']) is False:
            break
    validator(solution, ['*'])

    # mSemesters = next_solution_methods.MoveWholeChain(solution).start()
    json_obj = ExportJson(solution).get()
    return ExportJointjs(json_obj).get()
    # return ExportJson(solution).get_semester_list()
