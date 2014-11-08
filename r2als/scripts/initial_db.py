'''
initial_db
Description#   Initialize a database and test case
Developer#     Thada Wangthammang
'''
import os
import sys
import pymongo
import pprint


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

def createCategories(raw_categories):
    l.info("Creating categories")
    for raw_category in raw_categories:
        category = models.Category.objects(name=raw_category).first()
        if not category:
            category = models.Category()
            category.name = raw_category
            category.save()
        else:
            l.info("The categories is exist")
    return category

def createCurriculum(curriculum_data):
    curriculum = models.Curriculum()
    curriculum['faculty'] = curriculum_data['faculty']
    curriculum['department'] = curriculum_data['department']
    curriculum['year'] = int(curriculum_data['year'])
    curriculum['required_num_year'] = int(curriculum_data['required_num_year'])
    curriculum['num_semester'] = int(curriculum_data['num_semester'])
    l.info("Creating curriculum: "+ curriculum_data['department'] + " " + curriculum_data['year'])
    l.info("Adding Studied Group")
    for studied_group in curriculum_data['studied_groups']:
        curriculum['studied_groups'].append(studied_group)
    curriculum.save()
    return curriculum

def createSubject(raw_subjects, curriculum):
    l.info("Creating subjects & relationship between subjects")
    for raw_subject in raw_subjects:

        subject_tmp = models.Subject()

        # add a simple data
        if 'code' in raw_subject:
            subject_tmp.isSpecific = True
            subject_tmp.code = raw_subject['code']
        else:
            subject_tmp.isSpecific = False
            subject_tmp.code = ""
        subject_tmp.name = raw_subject['name']
        subject_tmp.credit = int(raw_subject.get('credit', '0'))
        # add curriculum
        subject_tmp.curriculum = curriculum

        # add categories
        if 'categories' in raw_subject:
            for category in raw_subject['categories']:
                mCategory = models.Category.objects(name=category).first()
                if mCategory is not None:
                    subject_tmp.categories.append(mCategory)
                else:
                    l.error('Not found "'+category+'" in collection')

        if 'studied_group' in raw_subject:
            subject_tmp.studied_group = raw_subject['studied_group']
        else : subject_tmp.studied_group = ''

        if 'year' in raw_subject: subject_tmp.year = int(raw_subject.get('year', '0'))
        else :
            l.error(raw_subject['name'] +"doesn't have year")
        if 'semester' in raw_subject: subject_tmp.semester = int(raw_subject.get('semester', '0'))
        else :
            l.error(raw_subject['name'] +"doesn't have semester")
        subject_tmp.save()

def linkAllSubject(raw_subjects):
    l.info("Linking all their relationship between subjects")
    for raw_subject in raw_subjects:

        if 'code' in raw_subject:
            subject_code = models.Subject.objects(code=raw_subject['code']).first()
            if 'studied_prerequisite' in raw_subject:
                for sp_code in raw_subject['studied_prerequisite']:
                    subject_code.studied_prerequisite.append(models.Subject.objects(code=sp_code).first())
            if 'passed_prerequisite' in raw_subject:
                for pp_code in raw_subject['passed_prerequisite']:
                    subject_code.passed_prerequisite.append(models.Subject.objects(code=pp_code).first())
            if 'corequisite' in raw_subject:
                for cr_code in raw_subject['corequisite']:
                    subject_code.corequisite.append(models.Subject.objects(code=cr_code).first())
            if 'cocurrent' in raw_subject:
                for cc_code in raw_subject['cocurrent']:
                    subject_code.corequisite.append(models.Subject.objects(code=cc_code).first())
            subject_code.save()

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
    raw_curriculum = importCurriculum2Model(config.data_path + curriculumPath)
    createCategories(raw_curriculum['info']['categories'])
    curriculum_model = createCurriculum(raw_curriculum['info'])
    createSubject(raw_curriculum['subjects'], curriculum_model)
    linkAllSubject(raw_curriculum['subjects'])

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


def main(isTest=False, curriculumPath='coe_2553_curriculum.csv'):
#if __name__ == '__main__':
    if len(sys.argv) != 2:
        # usage(sys.argv)
        sys.exit()

    configuration = config.Configurator(sys.argv[1])
    # config_uri = argv[1]
    # setup_logging(config_uri)
    # settings = get_appsettings(config_uri)
    models.initial(configuration.settings)
    print(configuration.settings)

    coe_curriculum_model = initialCoECurriculumData(curriculumPath)

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
