__author__ = 'mildronize'

import unittest
import random
import copy
from r2als import models
from r2als.libs.next_solution_method import NextSolutionMethod
from r2als.libs.solutions import InitialSolution
from r2als.libs.functions import *

SEED = 45

class TestNextSolutionMethod(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'test.ini')
        # configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)
        self.members = models.Member.objects()
        random.seed(SEED)

    # def tearDown(self):
        # models.Member.drop_collection()
        # models.Semester.drop_collection()

    def test_move_grade_subject(self):
        for member in self.members:
            si = SemesterIndex(member.curriculum.num_semester)
            solution = InitialSolution(member, random).get_solution()
            nsm = NextSolutionMethod(solution)
            for semester_iter in range(solution.member.num_studied_semester_id,
                                     len(solution.semesters)):
                for grade_subject in solution.semesters[semester_iter].subjects:
                    not_empty_semester_ids = solution.find_not_empty_semester_ids()
                    not_empty_semester_ids.remove(si.get(grade_subject.year, grade_subject.semester))
                    target_semester_id = not_empty_semester_ids[random.randint(0, len(not_empty_semester_ids)-1)]
                    before_gs = copy.copy(grade_subject)

                    print("Before "+extract_grade_subject(grade_subject))

                    before_num_subject = solution.countAllSubjects()
                    # Checking Moving must not fail
                    self.assertEqual(nsm.move_grade_subject(grade_subject, target_semester_id), True)
                    solution = nsm.get_solution()
                    # number of subject is not change
                    self.assertEqual(before_num_subject, solution.countAllSubjects())
                    subject = before_gs.subject
                    semester_id = si.get(before_gs.year, before_gs.semester)
                    # check the subject must store in correct semester
                    print("After "+extract_grade_subject(grade_subject))
                    self.assertEqual(solution.check_subject_exist(subject, semester_id), False)
                    self.assertEqual(solution.check_subject_exist(subject, target_semester_id), True)

    def test_swap_grade_subject(self):
        for member in self.members:
            si = SemesterIndex(member.curriculum.num_semester)
            solution = InitialSolution(member, random).get_solution()
            nsm = NextSolutionMethod(solution)
            for semester_iter in range(solution.member.num_studied_semester_id,
                                     len(solution.semesters)):
                for grade_subject in solution.semesters[semester_iter].subjects:
                    not_empty_semester_ids = solution.find_not_empty_semester_ids()
                    semester_id = not_empty_semester_ids[random.randint(0, len(not_empty_semester_ids)-1)]
                    grade_subject_id = random.randint(0, len(solution.semesters[semester_id].subjects)-1)
                    grade_subject_2 = solution.semesters[semester_id].subjects[grade_subject_id]
                    before_gs = copy.copy(grade_subject)
                    before_gs_2 = copy.copy(grade_subject_2)

                    print("Before "+extract_grade_subject(grade_subject) + " =-= " + extract_grade_subject(grade_subject_2))

                    before_num_subject = solution.countAllSubjects()
                    # Checking swapping must not fail
                    self.assertEqual(nsm.swap_grade_subject(grade_subject, grade_subject_2), True)
                    solution = nsm.get_solution()
                    # number of subject is not change
                    self.assertEqual(before_num_subject, solution.countAllSubjects())
                    subject = before_gs.subject
                    semester_id = si.get(before_gs.year, before_gs.semester)
                    subject_2 = before_gs_2.subject
                    semester_id_2 = si.get(before_gs_2.year, before_gs_2.semester)
                    # check the subject must store in correct semester
                    print("After "+extract_grade_subject(grade_subject) + " =-= " + extract_grade_subject(grade_subject_2))
                    self.assertEqual(solution.check_subject_exist(subject, semester_id_2), True)
                    self.assertEqual(solution.check_subject_exist(subject_2, semester_id), True)

