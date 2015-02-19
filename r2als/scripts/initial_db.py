'''
initial_db
Description#   Initialize a database and test case
Developer#     Thada Wangthammang
'''
import os
import sys
import pymongo
import pprint
from mongoengine import Q

from r2als.libs.logs import Log
from r2als.libs.solutions import InitialSolution
from r2als import models
from r2als import config
from r2als.libs.functions import SemesterIndex
# 2 types for importing library
# 1. from path/directory import package_name(*.py)
# 2. from path/package_name(*.py) import class_name
from r2als.scripts.convert_curriculum import CsvToModel

pp = pprint.PrettyPrinter(indent=4)
# lh = LogHandler()

 # setup `logging` module
l = Log('initial_db').getLogger()
# l.startApp('scripts/initial_db')

def import_curriculum_to_model(path):
    # Not check key yet
    return CsvToModel().process(path, True)

# def createCategories(raw_categories):
#     l.info("Creating categories")
#     for raw_category in raw_categories:
#         category = models.Category.objects(name=raw_category).first()
#         if not category:
#             category = models.Category()
#             category.name = raw_category
#             category.save()
#         else:
#             l.info("The categories is exist")
#     return category

def create_Curriculum(curriculum_data):
    curriculum = models.Curriculum()
    curriculum['faculty'] = curriculum_data['faculty']
    curriculum['department'] = curriculum_data['department']
    curriculum['year'] = int(curriculum_data['year'])
    curriculum['required_num_year'] = int(curriculum_data['required_num_year'])
    curriculum['max_year'] = int(curriculum_data['max_year'])
    curriculum['num_semester'] = int(curriculum_data['num_semester'])
    for not_force_enrolled_semester in curriculum_data['not_force_enrolled_semesters']:
        if int(not_force_enrolled_semester) > int(curriculum['num_semester']):
            l.error("not_force_enrolled_semester must <= num_semester")
        else:
            curriculum['not_force_enrolled_semesters'].append(int(not_force_enrolled_semester))
    l.info("Creating curriculum: "+ curriculum_data['department'] + " " + curriculum_data['year'])
    l.info("Creating Studied Group for the curriculum")
    for subject_group in curriculum_data['subject_groups']:
        curriculum['subject_groups'].append(subject_group)
    l.info("Adding categories for the curriculum")
    for categories in curriculum_data['categories']:
        curriculum['categories'].append(categories)
    curriculum.save()
    curriculum.reload()
    return curriculum

def create_SubjectGroup(subject_group, raw_subject, curriculum):
    mSubjectGroup = models.SubjectGroup()
    if 'subject_group' in raw_subject:
        mSubjectGroup.name = raw_subject['subject_group']
    elif subject_group is not '':
        mSubjectGroup.name = subject_group
    if 'year' in raw_subject:
        mSubjectGroup.year = int(raw_subject.get('year'))
    elif 'code' in raw_subject:
        l.error('The subject "%s" with having code ,that is specific subject, must have year field', raw_subject['name'])
    if 'semester' in raw_subject:
        mSubjectGroup.semester = int(raw_subject.get('semester'))
    elif 'code' in raw_subject:
        l.error('The subject "%s" with having code ,that is specific subject, must have semester field', raw_subject['name'])
    mSubjectGroup.curriculum = curriculum
    mSubjectGroup.save()
    mSubjectGroup.reload()
    return mSubjectGroup

def create_Subject(raw_subjects, curriculum):
    l.info("Creating subjects & relationship between subjects")
    for raw_subject in raw_subjects:
        # add a simple data
        if 'code' in raw_subject:
            subject_tmp = models.Subject.objects(code=raw_subject['code']).first()
            if subject_tmp is None:
                subject_tmp = models.Subject()
                subject_tmp.isSpecific = True
                subject_tmp.code = raw_subject['code']
        else:
            subject_tmp = models.Subject()
            subject_tmp.isSpecific = False
            subject_tmp.code = ""
        # add curriculum
        subject_tmp.curriculum = curriculum

        if 'subject_group' in raw_subject:
            # specific subject_group
            subject_tmp.subject_groups.append(create_SubjectGroup('', raw_subject, curriculum))
        else:
            # for all subject_group
            for subject_group in curriculum.subject_groups:
                subject_tmp.subject_groups.append(create_SubjectGroup(subject_group, raw_subject, curriculum))

        subject_tmp.name = raw_subject['name']
        subject_tmp.short_name = raw_subject['short_name']
        subject_tmp.credit = int(raw_subject.get('credit', '0'))

        # add categories
        if 'categories' in raw_subject:
            for category in raw_subject['categories']:
                subject_tmp.categories.append(category)
        subject_tmp.save()

def update_SubjectGroup(curriculum):
    for subject in models.Subject.objects(curriculum = curriculum):
        for subject_group in subject.subject_groups:
            subject_group.subject = subject
            subject_group.save()

def link_all_Subject(raw_curriculum):
    l.info("Linking all their relationship between subjects")
    processed_raw_subject = []
    for raw_subject in raw_curriculum['subjects']:
        if 'code' in raw_subject:
            subject_code = models.Subject.objects(code=raw_subject['code']).first()
            if raw_subject['code'] in processed_raw_subject:
                continue
            else:
                processed_raw_subject.append(raw_subject['code'])
            if subject_code:
                #linking subject
                for prerequisite_name in raw_curriculum['info']['prerequisites']:
                    if prerequisite_name in raw_subject:
                        for code in raw_subject[prerequisite_name]:
                            mPrerequisite = models.Prerequisite(name = prerequisite_name, subject = models.Subject.objects(code=code).first())
                            subject_code.prerequisites.append(mPrerequisite)
            subject_code.save()

def link_all_reverse_Subject(mCurriculum):
    l.info("Creating all their reverse relationship between subjects")
    subjects = models.Subject.objects(curriculum=mCurriculum, isSpecific = True)
    for subject in subjects:
        for prerequisites in subject.prerequisites:
            mPrerequisite = models.Prerequisite(name = prerequisites.name, subject = subject)
            prerequisites.subject.reverse_prerequisites.append(mPrerequisite)
            prerequisites.subject.save()

def create_Grade(grade_info):
    l.info("Adding grade")
    for grade in grade_info:
        grade_tmp = models.Grade()
        for key, value in grade.items():
            setattr(grade_tmp, key, value)
        grade_tmp.save()
    # print(models.Grade.objects().count())
    # return grade_tmp

def add_member(member):
    member_tmp = models.Member()
    for key, value in member['info'].items():
        member_tmp[key] = value
    member_tmp.save()
    l.info("Adding member: " + member['info']['name'])
    # adding EnrolledSemester
    for semester in member['semesters']:
        enrolledSemester = models.EnrolledSemester()
        enrolledSemester.year = semester['year']
        enrolledSemester.semester = semester['semester']

        for subject in semester['subjects']:

            if 'id' in subject:
                mSubject = models.Subject.objects(id = subject['id']).first()
                tmp_subject = subject['id']
            elif 'code' in subject:
                mSubject = models.Subject.objects(code = subject['code']).first()
                tmp_subject = subject['code']
            else:
                mSubject = None
                tmp_subject = None
                return None

            gradeSubject = models.GradeSubject()
            if mSubject is not None:
                gradeSubject.subject = mSubject
            else:
                l.error('Not found subject "%s"' % tmp_subject)
                return None
            mGrade = models.Grade.objects(name = subject['grade']).first()
            if mGrade is not None:
                gradeSubject.grade = mGrade
            else:
                l.error('Not found grade "%s"' % subject['grade'])
                return None
            enrolledSemester.subjects.append(gradeSubject)

        member_tmp.enrolled_semesters.append(enrolledSemester)
    member_tmp.save()
    member_tmp.reload()
    return member_tmp

def initial_coe_curriculum_data(curriculumPath):
    raw_curriculum = import_curriculum_to_model(curriculumPath)
    # createCategories(raw_curriculum['info']['categories'])
    curriculum_model = create_Curriculum(raw_curriculum['info'])
    create_Subject(raw_curriculum['subjects'], curriculum_model)
    update_SubjectGroup(curriculum_model)
    link_all_Subject(raw_curriculum)

    link_all_reverse_Subject(curriculum_model)

    print("")
    l.info("Adding some regulation and rule")

    # mustReEnroll is only main branch in each semester
    create_Grade([
        {'name': "A",  'score': 4.0, 'isCredit': True, 'canReEnroll': False,'mustReEnroll': False},
        {'name': "B+", 'score': 3.5, 'isCredit': True, 'canReEnroll': False,'mustReEnroll': False},
        {'name': "B",  'score': 3.0, 'isCredit': True, 'canReEnroll': False,'mustReEnroll': False},
        {'name': "C+", 'score': 2.5, 'isCredit': True, 'canReEnroll': False,'mustReEnroll': False},
        {'name': "C",  'score': 2.0, 'isCredit': True, 'canReEnroll': False,'mustReEnroll': False},
        {'name': "D+", 'score': 1.5, 'isCredit': True, 'canReEnroll': True, 'mustReEnroll': False},
        {'name': "D",  'score': 1.0, 'isCredit': True, 'canReEnroll': True, 'mustReEnroll': False},
        {'name': "E",  'score': 0.0, 'isCredit': True, 'canReEnroll': True, 'mustReEnroll': True},
        {'name': "S",                'isCredit': False,'canReEnroll': True, 'mustReEnroll': False},
        {'name': "U",                'isCredit': False,'canReEnroll': False,'mustReEnroll': True},
        {'name': "W",                'isCredit': False,'canReEnroll': False,'mustReEnroll': True, 'isEnrolled': False}
    ])
    return curriculum_model

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <curriculum_path>\n'
          '(example: "%s development.ini data/coe.csv")' % (cmd, cmd))
    sys.exit(1)


def main():
#if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv)
        sys.exit()

    curriculumPath = sys.argv[2]
    configuration = config.Configurator(sys.argv[1])
    models.initial(configuration.settings)

    coe_curriculum_model = initial_coe_curriculum_data(curriculumPath)

    subject_groups = models.SubjectGroup.objects(name = 'first-group',
                                                 curriculum = coe_curriculum_model,
                                                 ).order_by('year','semester')
    for subject_group in subject_groups:
        l.info('(%s/%s) [%s] %s',
               subject_group.year,
               subject_group.semester,
               subject_group.name,
               subject_group.subject.name)

    #initial test cases
    l.info("======== Starting initial test cases")
    #add a member
    testing_members = [

        {
            'info': {
                'member_id':'5710110997',
                'name' : 'Sangkaya Thaithai',
                'curriculum' : coe_curriculum_model,
                'subject_group' : 'first-group',
                'registered_year' : 2557,
                'last_year' : 1,
                'last_semester' : 1
                },
            'semesters' : [{
                'year': 1,
                'semester': 1,
                'subjects': [
                    # {'code' : '200-101','grade' : 'C'},
                    # {'code' : '242-101','grade' : 'C'},
                    # {'code' : '322-101','grade' : 'E'},  # E Math 1
                    # {'code' : '332-103','grade' : 'W'}, # W Drop Phy 1
                    # {'code' : '332-113','grade' : 'C'}, # Lab Phy 1
                    {'code' : '640-101','grade' : 'C'},
                    # {'code' : '890-101','grade' : 'C'},
                    ]
                }]
        }
    ]

    for testing_member in testing_members:
        add_member(testing_member)


        # {
        #     'info': {
        #         'member_id':'5710110999',
        #         'name' : 'Thongdee Mana',
        #         'curriculum' : coe_curriculum_model,
        #         'subject_group' : 'first-group',
        #         'registered_year' : 2557,
        #         'last_year' : 1,
        #         'last_semester' : 1,
        #         },
        #     'semesters' : [{
        #         'year': 1,
        #         'semester': 1,
        #         'subjects': [
        #             {'code' : '895-171','grade' : 'C'}, # subject from another semester
        #             {'code' : '200-101','grade' : 'C'},
        #             {'code' : '242-101','grade' : 'C'},
        #             {'code' : '322-101','grade' : 'C'},
        #             {'code' : '332-103','grade' : 'C'},
        #             {'code' : '332-113','grade' : 'C'},
        #             {'code' : '640-101','grade' : 'C'},
        #             {'code' : '890-101','grade' : 'C'},
        #             ]
        #         }]
        # },
        # {
        #     'info': {
        #         'member_id':'5710110998',
        #         'name' : 'Thongyib kondee',
        #         'curriculum' : coe_curriculum_model,
        #         'subject_group' : 'first-group',
        #         'registered_year' : 2557,
        #         'last_year' : 1,
        #         'last_semester' : 1,
        #         },
        #     'semesters' : [{
        #         'year': 1,
        #         'semester': 1,
        #         'subjects': [
        #             {'code' : '200-101','grade' : 'C'},
        #             {'code' : '242-101','grade' : 'C'},
        #             {'code' : '322-101','grade' : 'C'},
        #             {'code' : '332-103','grade' : 'C'},
        #             {'code' : '332-113','grade' : 'C'},
        #             {'code' : '640-101','grade' : 'C'},
        #             # not complete enrollment
        #             ]
        #         }]
        # },
