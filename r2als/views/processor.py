__author__ = 'mildronize'

from pyramid.view import view_config
from mongoengine import Q

from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import response_json
from r2als.scripts.initial_db import add_member

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
    result['subjects'] = []

    ##########################################################
    # checking request format (JSON)
    try:
        json_body = request.json_body
    except ValueError as e:
        l.error(e)
        return response_json({}, "error", "The request support only JSON format")

    ##########################################################
    # checking all keys
    if 'type' not in json_body:
        return response_json({}, "error", 'The request must have key "type"')
    elif 'semesters' not in json_body:
        return response_json({}, "error", 'The request must have key "semesters"')
    elif 'member' not in json_body:
        return response_json({}, "error", 'The request must have key "member"')

    ##########################################################

    type_data = json_body['type']
    semesters = json_body['semesters']
    member = json_body['member']

    if 'name' not in member:
        return response_json({}, "error", 'The request must have key "member.name"')
    if 'subject_group' not in member:
        return response_json({}, "error", 'The request must have key "member.subject_group"')

    if json_body['type'] == "array-of-semester":
        add_member(prepare_add_member(semesters, member))

    return response_json(result)