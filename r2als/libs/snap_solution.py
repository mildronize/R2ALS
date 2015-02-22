__author__ = 'mildronize'
from r2als import models
from r2als.libs.functions import SemesterIndex
import copy

class SnapSolution:

    def __init__(self, solution):
        si = SemesterIndex(solution.member.curriculum.num_semester)
        # self.solution = models.Solution()
        self.member = solution.member
        self.semesters = []
        self.score = int(solution.score)
        for semester_id in range(len(solution.semesters)):
            semester_obj = solution.semesters[semester_id]
            year = si.toYear(semester_id)
            semester = si.toSemester(semester_id)
            tmp_semester = models.Semester()
            tmp_semester.member = solution.member
            tmp_semester.year = year
            tmp_semester.semester = semester
            tmp_semester.subjects = []
            for grade_subject in semester_obj.subjects:
                tmp_grade_subject = models.GradeSubject()
                tmp_grade_subject.subject = grade_subject.subject
                if 'grade' in grade_subject:
                    tmp_grade_subject.grade = grade_subject.grade
                tmp_grade_subject.year = year
                tmp_grade_subject.semester = semester
                tmp_semester.subjects.append(tmp_grade_subject)

            self.semesters.append(tmp_semester)


