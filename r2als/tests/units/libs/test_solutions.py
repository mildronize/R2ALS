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
        solution = PreInitialSolution(member).start()
        # mSemesters = semesterList.semesters
        # count subject from curriculum
        subject_groups = models.SubjectGroup.objects(curriculum = member.curriculum,name = member.subject_group)
        # i=1
        # for subject_group in subject_groups:
        #     print( "%d) %d/%d: %s" % (i, subject_group.year, subject_group.semester,subject_group.subject.short_name))
        #     i +=1
        num_subject_from_curriculum = subject_groups.count()

        # count subject from InitialSolution (Generate)
        self.assertEqual(num_subject_from_curriculum,
                         solution.countNumEnrolledSubject())

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
