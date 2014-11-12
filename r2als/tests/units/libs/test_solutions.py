import unittest
from r2als import models
from r2als import config

class SolutionsTest(unittest.TestCase):

    def setUp(self):
        configuration = config.Configurator(config.root_path + 'test.ini')
        configuration.set('mongodb.is_remove_collections', True)
        models.initial(configuration.settings)
        models.Member.drop_collection()
        models.Semester.drop_collection()

    # test class InitialSolution
    def test_InitialSolution(self):
        from r2als.scripts import initial_db
        from r2als.libs.solutions import InitialSolution
        coe_curriculum_model = models.Curriculum.objects(department="Computer Engineering",year =2553).first()
        if coe_curriculum_model is None:
            print('Not found the curriculum')
            exit()
        testing_members = [
            # {
            #     'info': {
            #         'member_id':'5710110999',
            #         'name' : 'Thongdee Mana',
            #         'curriculum' : coe_curriculum_model,
            #         'studied_group' : 'first-group',
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
            #         'studied_group' : 'first-group',
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
            # }
            {
                'info': {
                    'member_id':'5710110997',
                    'name' : 'Sangkaya Thaithai',
                    'curriculum' : coe_curriculum_model,
                    'studied_group' : 'first-group',
                    'registered_year' : 2557,
                    'last_year' : 1,
                    'last_semester' : 1,
                    },
                'semesters' : [{
                    'year': 1,
                    'semester': 1,
                    'subjects': [
                        {'code' : '200-101','grade' : 'C'},
                        {'code' : '242-101','grade' : 'C'},
                        {'code' : '322-101','grade' : 'C'},
                        {'code' : '332-103','grade' : 'W'}, # Drop this subject
                        {'code' : '332-113','grade' : 'C'},
                        {'code' : '640-101','grade' : 'C'},
                        {'code' : '890-101','grade' : 'C'},
                        ]
                    }]
            }
        ]


        for testing_member in testing_members:
            member = initial_db.add_member(testing_member['info'])
            initialSolution = InitialSolution(member)
            # year/semester: 1/1
            for semester_info in testing_member['semesters']:
                initialSolution.addStudiedSubject(semester_info['year'], semester_info['semester'], semester_info['subjects'])

            initialSolution.start()
            # initialSolution.countImportedSubject()

            self.assertEqual(initialSolution.isCorrectInitialSolution(),True)
            self.assertEqual(initialSolution.countAllSubject(), initialSolution.countOnlyMemberSubject())


            # Run all data
            # todo : testing each case , There are 3 cases

    # InitialSolution
