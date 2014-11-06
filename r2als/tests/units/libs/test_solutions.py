import unittest

class SolutionsTest(unittest.TestCase):


    # test class InitialSolution
    def test_InitialSolution(self):
        from r2als.scripts import initial_db
        from r2als.libs.solutions import InitialSolution
        curriculumPath='coe_2553_curriculum.csv'
        # initial db for testing
        initial_db.initailModel(isTest=True, curriculumPath=curriculumPath)

        coe_curriculum_model = initial_db.initialCoECurriculumData(curriculumPath=curriculumPath)

        testing_members = [
            {
                'info': {
                    'member_id':'5710110999',
                    'name' : 'Thongdee Mana',
                    'curriculum' : coe_curriculum_model,
                    'studied_group' : 'first-group',
                    'registered_year' : 2557,
                    'last_num_year' : 1,
                    'last_semester' : 1,
                    },
                'semesters' : [{
                    'year': 1,
                    'semester': 1,
                    'subjects': [
                        {'code' : '200-101','grade' : 'C'},
                        {'code' : '242-101','grade' : 'C'},
                        {'code' : '322-101','grade' : 'C'},
                        {'code' : '332-103','grade' : 'C'},
                        {'code' : '332-113','grade' : 'C'},
                        {'code' : '640-101','grade' : 'C'},
                        {'code' : '890-101','grade' : 'C'},
                        {'code' : '895-171','grade' : 'C'}, # subject from another semester
                        ]
                    }]
            },{
                'info': {
                    'member_id':'5710110998',
                    'name' : 'Thongyib kondee',
                    'curriculum' : coe_curriculum_model,
                    'studied_group' : 'first-group',
                    'registered_year' : 2557,
                    'last_num_year' : 1,
                    'last_semester' : 1,
                    },
                'semesters' : [{
                    'year': 1,
                    'semester': 1,
                    'subjects': [
                        {'code' : '200-101','grade' : 'C'},
                        {'code' : '242-101','grade' : 'C'},
                        {'code' : '322-101','grade' : 'C'},
                        {'code' : '332-103','grade' : 'C'},
                        {'code' : '332-113','grade' : 'C'},
                        {'code' : '640-101','grade' : 'C'},
                        # not complete enrollment
                        ]
                    }]
            },{
                'info': {
                    'member_id':'5710110997',
                    'name' : 'Sangkaya Thaithai',
                    'curriculum' : coe_curriculum_model,
                    'studied_group' : 'first-group',
                    'registered_year' : 2557,
                    'last_num_year' : 1,
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
            initialSolution = InitialSolution(coe_curriculum_model, member)
            # year/semester: 1/1
            for semester_info in testing_member['semesters']:
                initialSolution.addStudiedSubject(semester_info['year'], semester_info['semester'], semester_info['subjects'])

            initialSolution.start()
            self.assertEqual(initialSolution.countAllSubject(), initialSolution.countOnlyMemberSubject())
            self.assertEqual(initialSolution.isCorrectInitialSolution(),True)

            # Run all data
            # todo : testing each case , There are 3 cases


    # InitialSolution
