__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als.libs.functions import *
l = Log('grade_subject_format').getLogger()

def grade_subject_format(solution):
    si = SemesterIndex(solution.member.curriculum.num_semester)
    for semester_id in range(len(solution.semesters)):
        semester = solution.semesters[semester_id]
        for grade_subject in semester.subjects:
            if grade_subject.year != semester.year or grade_subject.semester != semester.semester:
                l.error("%s is not correct format(%d/%d)" % (extract_grade_subject(grade_subject), semester.year, semester.semester))
                return False
            if semester_id != si.get(semester.year, semester.semester):
                l.error("Semester order incorrect")
                for id in range(semester_id , len(solution.semesters)):
                    l.error("Year: "+str(solution.semesters[id].year)+" Semester: "+str(solution.semesters[id].semester))
                return False
    return True
