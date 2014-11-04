'''
initial_db
Description#   Initialize a database and test case
Developer#     Thada Wangthammang
'''
import os
import sys
import pymongo
import pprint

from r2als.libs.logs import LogHandler
from r2als.libs.solutions import InitialSolution
from r2als import models
from r2als import config as cf
# 2 types for importing library
# 1. from path/directory import package_name(*.py)
# 2. from path/package_name(*.py) import class_name
from r2als.scripts.convert_curriculum import CsvToModel



pp = pprint.PrettyPrinter(indent=4)
lh = LogHandler()
lh.startApp('scripts/initial_db')

def importCurriculum2Model(path):
    # Not check key yet
    return CsvToModel().process(path, True)

def createDefaultCategories(default_categories):
    lh.info("Creating default categories")
    for default_category in default_categories:
        category = models.Category.objects(name=default_category).first()
        if not category:
            category = models.Category()
            category.name = default_category
            category.save()
        else:
            lh.info("The default categories is exist")
    return category

def createCurriculum(curriculum_data):
    curriculum = models.Curriculum()
    curriculum['faculty'] = curriculum_data['faculty']
    curriculum['department'] = curriculum_data['department']
    curriculum['year'] = int(curriculum_data['year'])
    curriculum['required_num_year'] = int(curriculum_data['required_num_year'])
    lh.info("Creating curriculum: "+ curriculum_data['department'] + " " + curriculum_data['year'])
    lh.info("Adding Studied Group")
    for studied_group in curriculum_data['studied_groups']:
        curriculum['studied_groups'].append(studied_group)
    curriculum.save()
    return curriculum

def createSubject(raw_subjects, curriculum):
    lh.info("Creating subjects & relationship between subjects")
    for raw_subject in raw_subjects:

        subject_tmp = models.Subject()

        # add a simple data
        if 'code' in raw_subject:
            subject_tmp.isSpecific = True
            subject_tmp.code = raw_subject['code']
        else:
            subject_tmp.isSpecific = False
        subject_tmp.name = raw_subject['name']
        subject_tmp.credit = int(raw_subject.get('credit', '0'))
        # add curriculum
        subject_tmp.curriculum = curriculum

        # add categories
        if 'categories' in raw_subject:
            for category in raw_subject['categories']:
                subject_tmp.categories.append(models.Category.objects(name=category).first())

        if 'studied_group' in raw_subject:
            subject_tmp.studied_group = raw_subject['studied_group']
        else : subject_tmp.studied_group = ''

        if 'year' in raw_subject: subject_tmp.year = int(raw_subject.get('year', '0'))
        else :
            lh.error(raw_subject['name'] +"doesn't have year")
        if 'semester' in raw_subject: subject_tmp.semester = int(raw_subject.get('semester', '0'))
        else :
            lh.error(raw_subject['name'] +"doesn't have semester")
        subject_tmp.save()

def linkAllSubject(raw_subjects):
    lh.info("Linking all their relationship between subjects")
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
    lh.info("Adding grade")
    for grade in grade_info:
        grade_tmp = models.Grade()
        for key, value in grade.items():
            grade_tmp[key] = value
        grade_tmp.save()
    return grade_tmp

def main():
#if __name__ == '__main__':
    # if len(argv) != 2:
    #     usage(argv)
    # config_uri = argv[1]
    # setup_logging(config_uri)
    # settings = get_appsettings(config_uri)

    raw_curriculum = importCurriculum2Model('data/coe_2553_curriculum.csv')
    raw_subjects = raw_curriculum['subjects']
    curriculum_data = raw_curriculum['info']

    models.initial({'mongodb.db_name':cf.Config.db_name,'mongodb.host':cf.Config.host,'mongodb.is_reset':cf.Config.is_reset})

    createDefaultCategories(['lecture', 'lab','project'])

    coe_curriculum_model = createCurriculum(curriculum_data)

    createSubject(raw_subjects, coe_curriculum_model)

    linkAllSubject(raw_subjects)

    ####################################################
    print("")
    lh.info("Adding some regulation and rule")

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

    ####################################################
    print("")
    #initial test cases
    lh.info("Starting initial test cases")
    #add a member
    member_thongdee = models.Member()
    member_thongdee.member_id = '5710110999'
    member_thongdee.name = 'Thongdee Mana'
    member_thongdee.curriculum = coe_curriculum_model
    member_thongdee.studied_group = 'first-group'
    member_thongdee.registered_year = 2557
    member_thongdee.last_num_year = 1
    member_thongdee.last_semester = 1
    lh.info("Adding member: " + member_thongdee.name)
    member_thongdee.save()

    #add dummy data (thongdee)
    lh.info("Starting to generate the Initial Solution of him")
    initialSolution = InitialSolution(coe_curriculum_model, member_thongdee)
    # year/semester: 1/1

    initialSolution.addStudiedSubject(1,1,[
        {'code' : '200-101','grade' : 'C'},
        {'code' : '242-101','grade' : 'C'},
        {'code' : '322-101','grade' : 'W'},
        {'code' : '332-103','grade' : 'C'},
        {'code' : '332-113','grade' : 'C'},
        {'code' : '640-101','grade' : 'C'},
        {'code' : '890-101','grade' : 'C'}
    ])
    # initialSolution.addStudiedSubject(2,1,[
    #     {'code' : '242-205','grade' : 'C'}
    #
    # ])
    initialSolution.start()


    lh.close()
