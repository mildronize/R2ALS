__author__ = 'mildronize'

from pyramid.view import view_config

from r2als import models
from r2als.libs.solutions import InitialSolution
from r2als.libs.exports import ExportJson, ExportJointjs
from r2als.libs import next_solution_methods

@view_config(route_name='solution_generator', renderer='/solution_generator/index.mako')
def index(request):

    return dict(
                test_text = "Hello wolrd!"
                )

@view_config(route_name='apis.solution_generator',renderer='json')
def solution_generator_api_json(request):

    member = models.Member.objects(member_id = '5710110997').first()
    if member is None:
        print('Not found the member')
        exit()

    semesterList = InitialSolution(member).start()
    mSemesters = next_solution_methods.MoveWholeChain(semesterList).start()

    json_obj = ExportJson(member, mSemesters).get()
    return ExportJointjs(json_obj).get()