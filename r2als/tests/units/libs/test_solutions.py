import unittest
from r2als import models
from r2als import config

class SolutionsTest(unittest.TestCase):

    def setUp(self):
        configuration = config.Configurator(config.root_path + 'test.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

    # def tearDown(self):

        # models.Member.drop_collection()
        # models.Semester.drop_collection()

    # test class InitialSolution
    def test_InitialSolution(self):
        from r2als.libs.solutions import InitialSolution
        member = models.Member.objects(member_id = '5710110997').first()
        if member is None:
            print('Not found the member')
            exit()
        mSemesters = InitialSolution(member)

        # count subject from curriculum
        num_subject_from_curriculum = models.StudiedGroup.objects(curriculum = member.curriculum,
                                                                  name = member.studied_group).count()

        # count subject from InitialSolution (Generate)
        num_subject_from_generate = 0
        for mSemester in mSemesters:
            num_subject_from_generate += len(mSemester.subjects)

        self.assertEqual(num_subject_from_curriculum,
                         num_subject_from_generate)

        # test num of subject each semester
        for mSemester in mSemesters:
            num_subject_from_curriculum = models.StudiedGroup.objects(curriculum = member.curriculum,
                                                      name = member.studied_group,
                                                      year = mSemester.year,
                                                      semester = mSemester.semester).count()
            num_subject_from_generate = len(mSemester.subjects)
            self.assertEqual(num_subject_from_curriculum,
                             num_subject_from_generate)

        # self.assertEqual(initialSolution.isCorrectInitialSolution(),True)
        # self.assertEqual(initialSolution.countAllSubject(), initialSolution.countOnlyMemberSubject())


            # Run all data
            # todo : testing each case , There are 3 cases


    # InitialSolution
