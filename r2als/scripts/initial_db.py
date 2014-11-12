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
# 2 types for importing library
# 1. from path/directory import package_name(*.py)
# 2. from path/package_name(*.py) import class_name
from r2als.scripts.convert_curriculum import CsvToModel

pp = pprint.PrettyPrinter(indent=4)
# lh = LogHandler()

 # setup `logging` module
l = Log('initial_db').getLogger()
# l.startApp('scripts/initial_db')

def importCurriculum2Model(path):
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

def createCurriculum(curriculum_data):
    curriculum = models.Curriculum()
    curriculum['faculty'] = curriculum_data['faculty']
    curriculum['department'] = curriculum_data['department']
    curriculum['year'] = int(curriculum_data['year'])
    curriculum['required_num_year'] = int(curriculum_data['required_num_year'])
    curriculum['num_semester'] = int(curriculum_data['num_semester'])
    l.info("Creating curriculum: "+ curriculum_data['department'] + " " + curriculum_data['year'])
    l.info("Creating Studied Group for the curriculum")
    for studied_group in curriculum_data['studied_groups']:
        curriculum['studied_groups'].append(studied_group)
    l.info("Adding categories for the curriculum")
    for categories in curriculum_data['categories']:
        curriculum['categories'].append(categories)
    curriculum.save()
    curriculum.reload()
    return curriculum

def createStudiedGroup(studied_group, raw_subject, curriculum):
    mStudiedGroup = models.StudiedGroup()
    if 'studied_group' in raw_subject:
        mStudiedGroup.name = raw_subject['studied_group']
    elif studied_group is not '':
        mStudiedGroup.name = studied_group
    if 'year' in raw_subject:
        mStudiedGroup.year = int(raw_subject.get('year'))
    elif 'code' in raw_subject:
        l.error('The subject "%s" with having code ,that is specific subject, must have year field', raw_subject['name'])
    if 'semester' in raw_subject:
        mStudiedGroup.semester = int(raw_subject.get('semester'))
    elif 'code' in raw_subject:
        l.error('The subject "%s" with having code ,that is specific subject, must have semester field', raw_subject['name'])
    mStudiedGroup.curriculum = curriculum
    mStudiedGroup.save()
    mStudiedGroup.reload()
    return mStudiedGroup

def createSubject(raw_subjects, curriculum):
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

        if 'studied_group' in raw_subject:
            # specific studied_group
            subject_tmp.studied_groups.append(createStudiedGroup('', raw_subject, curriculum))
            # subject_tmp.add_studied_groups(raw_subject['studied_group'], raw_subject['year'], raw_subject['semester'])
        else:
            # for all studied_group
            for studied_group in curriculum.studied_groups:
                # subject_tmp.add_studied_groups(studied_group, raw_subject['year'], raw_subject['semester'])
                subject_tmp.studied_groups.append(createStudiedGroup(studied_group, raw_subject, curriculum))

        subject_tmp.name = raw_subject['name']
        subject_tmp.credit = int(raw_subject.get('credit', '0'))

        # add categories
        if 'categories' in raw_subject:
            for category in raw_subject['categories']:
                subject_tmp.categories.append(category)
        subject_tmp.save()

def updateStudiedGroup(curriculum):
    for subject in models.Subject.objects(curriculum = curriculum):
        for studied_group in subject.studied_groups:
            studied_group.subject = subject
            studied_group.save()

def linkAllSubject(raw_curriculum):
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
            # if 'studied_prerequisite' in raw_subject:
            #     for sp_code in raw_subject['studied_prerequisite']:
            #         subject_code.studied_prerequisite.append(models.Subject.objects(code=sp_code).first())
            # if 'passed_prerequisite' in raw_subject:
            #     for pp_code in raw_subject['passed_prerequisite']:
            #         subject_code.passed_prerequisite.append(models.Subject.objects(code=pp_code).first())
            # if 'corequisite' in raw_subject:
            #     for cr_code in raw_subject['corequisite']:
            #         subject_code.corequisite.append(models.Subject.objects(code=cr_code).first())
            # if 'cocurrent' in raw_subject:
            #     for cc_code in raw_subject['cocurrent']:
            #         subject_code.corequisite.append(models.Subject.objects(code=cc_code).first())
            subject_code.save()

def linkAllReverseSubject(mCurriculum):
    l.info("Creating all their reverse relationship between subjects")
    subjects = models.Subject.objects(curriculum=mCurriculum, isSpecific = True)
    for subject in subjects:
        for prerequisites in subject.prerequisites:
            mPrerequisite = models.Prerequisite(name = prerequisites.name, subject = subject)
            prerequisites.subject.reverse_prerequisites.append(mPrerequisite)
            prerequisites.subject.save()

def createGrade(grade_info):
    l.info("Adding grade")
    for grade in grade_info:
        grade_tmp = models.Grade()
        for key, value in grade.items():
            setattr(grade_tmp, key, value)
        grade_tmp.save()
    # print(models.Grade.objects().count())
    # return grade_tmp

def add_member(member_info):
    member_tmp = models.Member()
    for key, value in member_info.items():
        member_tmp[key] = value
    member_tmp.save()
    l.info("Adding member: " + member_info['name'])
    member_tmp.save()
    member_tmp.reload()
    return member_tmp

def initialCoECurriculumData(curriculumPath):
    raw_curriculum = importCurriculum2Model(curriculumPath)
    # createCategories(raw_curriculum['info']['categories'])
    curriculum_model = createCurriculum(raw_curriculum['info'])
    createSubject(raw_curriculum['subjects'], curriculum_model)
    updateStudiedGroup(curriculum_model)
    linkAllSubject(raw_curriculum)

    linkAllReverseSubject(curriculum_model)

    print("")
    l.info("Adding some regulation and rule")

    # mustReEnroll is only main branch in each semester
    createGrade([
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
        {'name': "W",                'isCredit': False,'canReEnroll': False,'mustReEnroll': True}
    ])
    return curriculum_model

# def initailModel(isTest=False, curriculumPath='coe_2553_curriculum.csv'):
#     if isTest == False: db_name = config.db_name
#     else: db_name = config.db_name_test
#     models.initial({'mongodb.db_name':db_name,'mongodb.host':config.host,'mongodb.is_reset':config.is_reset})

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
    # config_uri = argv[1]
    # setup_logging(config_uri)
    # settings = get_appsettings(config_uri)
    models.initial(configuration.settings)
    print(configuration.settings)

    coe_curriculum_model = initialCoECurriculumData(curriculumPath)

    # print(models.Subject.objects(curriculum=coe_curriculum_model).count())
    # subjects = models.Subject.objects(curriculum=coe_curriculum_model)
    # Q(code='324-103') | Q(code='322-101') &
    subject_tmp = models.Subject(code='324-103')
    studied_groups = models.StudiedGroup.objects(name = 'first-group',
                                                 curriculum = coe_curriculum_model,
                                                 ).order_by('year','semester')
    # subjects = sorted(subjects, key=attrgetter('studied_groups.year'))
    # .order_by('studied_groups__year','studied_groups__semester')
    # print(len(studied_groups))
    for studied_group in studied_groups:
        l.info('(%s/%s) [%s] %s',
               studied_group.year,
               studied_group.semester,
               studied_group.name,
               studied_group.subject.name)

        # l.info('(%s/%s) [%s] %s',subject.get_studied_group('second-group').year,s_ubject.get_studied_group('second-group').semester,subject.get_studied_group('second-group').name,subject.name)
        # print("-----")
        # l.info('(%s/%s) [%s] %s',subject.studied_groups['first-group'].year)
        # pp.pprint(subject.__dict__)
    #     for prerequisite in subject.prerequisites:
    #         l.info('%s is prerequisite = %s (%s)',subject.name ,prerequisite.subject.name, prerequisite.name)
    #     l.info('%s %s',subject.name,len(subject.reverse_prerequisites))
    #     for reverse_prerequisite in subject.reverse_prerequisites:
    #         l.info('%s is reverse-prereq = %s (%s)',subject.name ,reverse_prerequisite.subject.name, reverse_prerequisite.name)

    # studiedGroups =  models.StudiedGroup.objects( curriculum = coe_curriculum_model, name='first-group').order_by('year', 'semester')
    # for studiedGroup in studiedGroups:
    #     l.info('(%s/%s) %s',studiedGroup.year,studiedGroup.semester,studiedGroup.subject.name)

    # subjects = models.Subject.objects(curriculum = coe_curriculum_model)


    #initial test cases
    # l.info("Starting initial test cases")
    # #add a member
    # member_thongdee = add_member({
    #     'member_id':'5710110999',
    #     'name' : 'Thongdee Mana',
    #     'curriculum' : coe_curriculum_model,
    #     'studied_group' : 'first-group',
    #     'registered_year' : 2557,
    #     'last_num_year' : 1,
    #     'last_semester' : 1,
    # })
    #
    # #add dummy data (thongdee)
    # l.info("Starting to generate the Initial Solution of him")
    # initialSolution = InitialSolution(coe_curriculum_model, member_thongdee)
    # # year/semester: 1/1
    #
    # initialSolution.addStudiedSubject(1,1,[
    #     {'code' : '200-101','grade' : 'C'},
    #     {'code' : '242-101','grade' : 'C'},
    #     {'code' : '322-101','grade' : 'W'},
    #     {'code' : '332-103','grade' : 'C'},
    #     {'code' : '332-113','grade' : 'C'},
    #     {'code' : '640-101','grade' : 'C'},
    #     {'code' : '890-101','grade' : 'C'}
    # ])
    # # initialSolution.addStudiedSubject(2,1,[
    # #     {'code' : '242-205','grade' : 'C'}
    # #
    # # ])
    # initialSolution.start()
