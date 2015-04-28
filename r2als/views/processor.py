__author__ = 'mildronize'

from pyramid.view import view_config
from mongoengine import Q

from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import response_json, SemesterIndex
from r2als.scripts.initial_db import add_member
from r2als.engines.processor import Processor
from r2als.libs.exports import ExportJson, ExportJointjs
from r2als.libs.validators.prerequisite_check import prerequisite_check
from r2als.libs.solutions import PreInitialSolution

l = Log("view/processor").getLogger()

def prepare_add_member(semesters, member):
    tmp_info = dict()
    tmp_info['member_id'] = member['name']
    tmp_info['name'] = member['name']
    tmp_info['curriculum'] = models.Curriculum.objects().first()
    tmp_info['subject_group'] = member['subject_group']
    tmp_info['registered_year'] = 2557
    tmp_info['last_year'] = int(semesters[len(semesters) - 1]['year'])
    tmp_info['last_semester'] = int(semesters[len(semesters) - 1]['semester'])
    tmp_semesters = []
    for semester in semesters:
        tmp_semester = dict()
        tmp_semester['year'] = semester['year']
        tmp_semester['semester'] = semester['semester']
        tmp_semester['subjects'] = []
        for subject in semester['subjects']:
            tmp_subject = dict()
            tmp_subject['id'] = subject['id']
            tmp_subject['grade'] = subject['grade']
            tmp_semester['subjects'].append(tmp_subject)
        tmp_semesters.append(tmp_semester)
    return {
        'info': tmp_info,
        'semesters': tmp_semesters
    }


@view_config(route_name='apis.processor', renderer='json')
def index(request):
    result = dict()
    result['plans'] = []
    is_testing = False

    ##########################################################
    # checking request format (JSON)
    try:
        json_body = request.json_body
    except ValueError as e:
        l.error(e)
        return response_json({}, "error", ["The request support only JSON format"])

    ##########################################################
    # checking all keys
    if 'is_testing' not in json_body:
        return response_json({}, "error", ['The request must have key "is_testing"'])

    if json_body['is_testing'] == True:
        is_testing = json_body['is_testing']
    else:
        if 'type' not in json_body:
            return response_json({}, "error", ['The request must have key "type"'])
        elif 'semesters' not in json_body:
            return response_json({}, "error", ['The request must have key "semesters"'])
        elif 'member' not in json_body:
            return response_json({}, "error", ['The request must have key "member"'])
        elif 'is_testing' in json_body:
            is_testing = json_body['is_testing']


        ##########################################################

        type_data = json_body['type']
        semesters = json_body['semesters']
        member = json_body['member']

        if 'name' not in member:
            return response_json({}, "error", ['The request must have key "member.name"'])
        if 'subject_group' not in member:
            return response_json({}, "error", ['The request must have key "member.subject_group"'])
        if len(semesters) == 0:
            return response_json({}, "error", ['Please add your enrolled subjects.'])

        if json_body['type'] != "array-of-semester":
            return response_json({}, "error", ['The type of data allows only "array-of-semester"'])



    # End checking
    ##########################################################
    # for testing

    if is_testing == True:
        member = models.Member.objects(member_id="testcase4").first()
        if member is None:
            return response_json({}, "error", ['Can\'t run testing mode because no member in database'])
        si = SemesterIndex(member.curriculum.num_semester)

    else:
        member = add_member(prepare_add_member(semesters, member))
        if member is None:
            return response_json({}, "error", ['Can\'t add member'])


        count_semester = 0
        si = SemesterIndex(member.curriculum.num_semester)
        for semester in semesters:
            check = True
            for not_force_enrolled_semester in member.curriculum.not_force_enrolled_semesters:
                if semester['semester'] == not_force_enrolled_semester:
                    check = False
                    break
            if check:
                count_semester += 1

        count_not_force_enrolled_semesters = si.count_specific_semesters(len(semesters), member.curriculum.not_force_enrolled_semesters)
        if count_semester + count_not_force_enrolled_semesters != len(semesters):
            return response_json({}, "error", ['Please checking your enrollment'])


    # checking the enrollment is possible
    # checking_solution = PreInitialSolution(member).get_solution()
    #
    # # result['plans'].append(ExportJson(checking_solution).get_semester_list())
    # # return response_json(result)
    #
    # problem_subjects = prerequisite_check(checking_solution, quick_checking=False, check_studied_semester_only=True)
    # if len(problem_subjects) != 0:
    #     tmp = ['Impossible enrollment:']
    #     for problem_subject in problem_subjects:
    #         tmp_message = 'Because "%s" is not %s of "%s"' % (problem_subject['prerequisite_grade_subject'].subject.name,
    #                                                         problem_subject['prerequisite'],
    #                                                         problem_subject['grade_subject'].subject.name)
    #         tmp.append(tmp_message)
    #     return response_json({}, "error", tmp)

    l.info("ahaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    seed = 37
    # 37,107,257,521
    solutions = Processor(member, 20, 20, seed).start()

    for solution in solutions:
        result['plans'].append(ExportJson(solution).get_semester_list())
    # solution = PreInitialSolution(member).get_solution()
    # result['plans'].append(ExportJson(solution).get_semester_list())
    return response_json(result)

