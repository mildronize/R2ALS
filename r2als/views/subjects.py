__author__ = 'mildronize'

from pyramid.view import view_config
from mongoengine import Q

from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import response_json

l = Log("view/subjects").getLogger()

@view_config(route_name='apis.subjects', renderer='json')
def index(request):
    result = dict()
    result['subjects'] = []

    subjects = models.Subject.objects()
    for subject in subjects:
        result['subjects'].append({
            'name': subject.name
        })
    return response_json(result)

@view_config(route_name='apis.subjects.search', renderer='json')
def subjects_search(request):
    query_string = str(request.matchdict.get('query_string'))
    l.info(query_string)
    result = dict()
    result['subjects'] = []
    # simple query
    subjects = models.Subject.objects((Q(name__icontains=query_string) | Q(code__icontains=query_string)) & Q(isSpecific=True))
    for subject in subjects:
        result['subjects'].append({
            'id': str(subject.id),
            'name': subject.name,
            'code': subject.code
        })
    return response_json(result)

@view_config(route_name='apis.subject_groups.search', renderer='json')
def subject_groups_search(request):
    query_string = str(request.matchdict.get('query_string'))
    subject_group = str(request.matchdict.get('subject_group'))
    l.info(query_string)
    l.info(subject_group)
    result = dict()
    result['subjects'] = []

    subjects = models.Subject.objects((Q(name__icontains=query_string) | Q(code__icontains=query_string)) & Q(isSpecific=True))
    for subject in subjects:
        tmp = {
            'id': str(subject.id),
            'name': subject.name,
            'code': subject.code
        }
        query_subject_group = models.SubjectGroup.objects(subject=subject ,name=subject_group).first()
        if query_subject_group is not None:
            tmp['year'] = query_subject_group.year
            tmp['semester'] = query_subject_group.semester
        result['subjects'].append(tmp)
    return response_json(result)

