import unittest
from r2als import models

class SolutionsTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

    # def tearDown(self):

        # models.Member.drop_collection()
        # models.Semester.drop_collection()

    # test class InitialSolution
    def test_PreInitialSolution(self):
        # Not test now

        from r2als.libs.solutions import PreInitialSolution
        member = models.Member.objects(member_id = '5710110997').first()
        if member is None:
            print('Not found the member')
            exit()
        solution = PreInitialSolution(member).get_solution()

        grade_subjects = []
        for grade_subject in solution.get_grade_subjects():
            grade_subjects.append(str(grade_subject.subject.id))
        all_subjects = []
        for subject_group in models.SubjectGroup.objects(curriculum = member.curriculum,name = member.subject_group):
            all_subjects.append(str(subject_group.subject.id))

        # count subject from InitialSolution (Generate)
        tmp_diff_lists = list(set(all_subjects) - set(grade_subjects))
        # if len(tmp_diff_lists) > 0:
        #     for tmp_subject in tmp_diff_lists:
                # l.info(self.findSubjectById(tmp_subject).short_name +"\t\t is enrolled over than the curriculum")
        # self.assertEqual(num_subject_from_curriculum,
        #                  solution.countNumEnrolledSubject())
        self.assertEqual(len(tmp_diff_lists), 0)

        # test num of subject each semester
        # for mSemester in mSemesters:
        #     num_subject_from_curriculum = models.SubjectGroup.objects(curriculum = member.curriculum,
        #                                                               name = member.subject_group,
        #                                                               semester_id__year = mSemester.semester_id.year,
        #                                                               semester_id__semester = mSemester.semester_id.semester).count()
        #     num_subject_from_generate = len(mSemester.subjects)
        #     self.assertEqual(num_subject_from_curriculum,
        #                      num_subject_from_generate)

        # self.assertEqual(initialSolution.isCorrectInitialSolution(),True)
        # self.assertEqual(initialSolution.countAllSubject(), initialSolution.countOnlyMemberSubject())

            # Run all data
            # todo : testing each case , There are 3 cases


    # InitialSolution
