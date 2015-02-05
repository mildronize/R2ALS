__author__ = 'mildronize'

from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import *
from r2als.libs import prerequisites
l = Log('prerequisite_check').getLogger()

def prerequisite_check(solution):
    # l.info("prerequisite_check is validating...")
    si = SemesterIndex(solution.member.curriculum.num_semester)

    for current_semester_id in reversed(range(solution.member.num_studied_semester_id, len(solution.semesters))):
        semester_item = solution.semesters[current_semester_id]
        for grade_subject in semester_item.subjects:
            if grade_subject.subject.prerequisites != []:
                for prerequisite in grade_subject.subject.prerequisites:
                    # Not consider studied semester
                    if si.get(prerequisite.grade_subject.year, prerequisite.grade_subject.semester) >= current_semester_id:
                        p = prerequisites.selector(prerequisite.name,
                                                   prerequisite.grade_subject,
                                                   grade_subject,
                                                   solution.member)
                        if p.canEnrolled() is False:
                            l.info("Because %s is not %s of %s" % (extract_grade_subject(prerequisite.grade_subject),
                                                                   prerequisite.name,
                                                                   extract_grade_subject(grade_subject)))
                            return False
    return True
