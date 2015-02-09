__author__ = 'mildronize'

from r2als.libs.logs import Log
l = Log('grade_subject_format').getLogger()

def grade_subject_format(solution):
    for semester in solution.semesters:
        for grade_subject in semester.subjects:
            if grade_subject.year != semester.year or grade_subject.semester != semester.semester:
                return False
    return True
