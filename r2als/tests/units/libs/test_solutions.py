import unittest
from r2als import models
from r2als.libs.solutions import PreInitialSolution

# parameter for testing
NUM_SEMESTER = 3

# todo: test PreInitialSolution.addSemesterModel()
# todo: test PreInitialSolution.get_solution()

class SolutionsTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'test.ini')
        # configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)
        self.members = models.Member.objects()

    # def tearDown(self):
        # models.Member.drop_collection()
        # models.Semester.drop_collection()

    #=====  Start functional test =====
    # test class PreInitialSolution (func)

    def test_PreInitialSolution(self):

        for member in self.members:
            solution = PreInitialSolution(member).get_solution()
            grade_subjects = []
            for grade_subject in solution.get_grade_subjects():
                grade_subjects.append(str(grade_subject.subject.id))
            all_subjects = []
            for subject_group in models.SubjectGroup.objects(curriculum=member.curriculum,
                                                             name=member.subject_group):
                all_subjects.append(str(subject_group.subject.id))

            # count subject from InitialSolution (Generate)
            tmp_diff_lists = list(set(all_subjects) - set(grade_subjects))

            self.assertEqual(len(tmp_diff_lists), 0)

    # =====  end functional test =====

        # if len(tmp_diff_lists) > 0:
        #     for tmp_subject in tmp_diff_lists:
                # l.info(self.findSubjectById(tmp_subject).short_name +"\t\t is enrolled over than the curriculum")
        # self.assertEqual(num_subject_from_curriculum,
        #                  solution.countNumEnrolledSubject())
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


    def test_initial_empty_year(self):
        for member in self.members:
            self.assertEqual(NUM_SEMESTER, member.curriculum.num_semester)
            semesters = PreInitialSolution(member).initial_empty_year()
            for semester in semesters:
                self.assertEqual(len(semester), 0)

    def test_has_imported_subject(self):
        member = self.members[0]
        pis = PreInitialSolution(member)
        self.assertEqual(len(pis.imported_subject), 0)
        pis.imported_subject.append("subject_id_test")
        pis.imported_subject.append("subject_id_test1")
        pis.imported_subject.append("subject_id_test2")
        self.assertEqual(pis.has_imported_subject("subject_id_test"), True)
        self.assertEqual(pis.has_imported_subject("subject_id_test_false"), False)
        self.assertEqual(pis.has_imported_subject("subject_id_test2"), True)

    def test_add_imported_subject(self):
        member = self.members[0]
        pis = PreInitialSolution(member)
        self.assertEqual(len(pis.imported_subject), 0)
        self.assertEqual(pis.add_imported_subject("subject_id_test"), True)
        self.assertEqual(pis.add_imported_subject("subject_id_test1"), True)
        self.assertEqual(pis.add_imported_subject("subject_id_test2"), True)
        self.assertEqual(pis.add_imported_subject("subject_id_test"), False)
        self.assertEqual(pis.add_imported_subject("subject_id_test1"), False)
        self.assertEqual(pis.add_imported_subject("subject_id_test2"), False)

    def test_count_remain_subjects(self):
        member = self.members[0]
        pis = PreInitialSolution(member)
        self.assertEqual(len(pis.remain_subjects), member.curriculum.num_semester)
        pis.remain_subjects[0].append("subject_id_test")
        self.assertEqual(pis.count_remain_subjects(), 1)
        pis.remain_subjects[1].append("subject_id_test")
        self.assertEqual(pis.count_remain_subjects(), 2)
        pis.remain_subjects[2].append("subject_id_test")
        self.assertEqual(pis.count_remain_subjects(), 3)
        pis.remain_subjects[1].append("subject_id_test2")
        pis.remain_subjects[1].append("subject_id_test3")
        self.assertEqual(pis.count_remain_subjects(), 5)

    # InitialSolution
