__author__ = 'mildronize'

from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import *
from r2als.libs import prerequisites
l = Log('prerequisite_check').getLogger()

# todo: Change this function into Class

def prerequisite_check(solution, quick_checking=True, isReversed=True):
    l.info("prerequisite_check is validating ...")
    if quick_checking:
        l.info("Quick checking mode")
    invalid_grade_subjects = []
    if isReversed:
        range_finding = reversed(range(solution.member.num_studied_semester_id, len(solution.semesters)))
    else:
        range_finding = range(solution.member.num_studied_semester_id, len(solution.semesters))
    si = SemesterIndex(solution.member.curriculum.num_semester)
    for current_semester_id in range_finding:
        # l.info("semester_id %d " % current_semester_id)
        semester_item = solution.semesters[current_semester_id]
        for grade_subject in semester_item.subjects:
            # if grade_subject.subject.prerequisites != []:
            # l.debug("Checking... " +extract_grade_subject(grade_subject))
            for prerequisite in grade_subject.subject.prerequisites:
                l.debug(extract_grade_subject(prerequisite.grade_subject) + " <----- " + extract_grade_subject(grade_subject))
                # Not consider studied semester
                if si.get(prerequisite.grade_subject.year, prerequisite.grade_subject.semester) > solution.member.num_studied_semester_id - 1:
                    p = prerequisites.selector(prerequisite.name,
                                               prerequisite.grade_subject,
                                               grade_subject,
                                               solution.member)
                    if p.canEnrolled() is False:
                        l.info("Because %s is not %s of %s" % (extract_grade_subject(prerequisite.grade_subject),
                                                               prerequisite.name,
                                                               extract_grade_subject(grade_subject)))
                        if quick_checking:
                            return False
                        tmp = dict()
                        tmp['prerequisite_grade_subject'] = prerequisite.grade_subject
                        tmp['grade_subject'] = grade_subject
                        invalid_grade_subjects.append(tmp)
                    # else:
                    #     l.debug("List of subject prerequisite is pass testing:")
                    #     l.debug(extract_grade_subject(prerequisite.grade_subject))
    if quick_checking:
        return True
    else:
        return invalid_grade_subjects


# def __is_prerequisite(member ,grade_subject, prerequisite):
#     p = prerequisites.selector(prerequisite.name,
#                                prerequisite.grade_subject,
#                                grade_subject,
#                                member)
#     if p.canEnrolled() is False:
#         l.info("Because %s is not %s of %s" % (extract_grade_subject(prerequisite.grade_subject),
#                                                prerequisite.name,
#                                                extract_grade_subject(grade_subject)))
#         return False
#     return True

# def __find_invalid_grade_subjects(solution):
#     invalid_subjects = []
#     si = SemesterIndex(solution.member.curriculum.num_semester)
#     for current_semester_id in reversed(range(solution.member.num_studied_semester_id, len(solution.semesters))):
#         semester_item = solution.semesters[current_semester_id]
#         for grade_subject in semester_item.subjects:
#             if grade_subject.subject.prerequisites != []:
#                 for prerequisite in grade_subject.subject.prerequisites:
#                     # Not consider studied semester
#                     if si.get(prerequisite.grade_subject.year, prerequisite.grade_subject.semester) >= current_semester_id:
#                         invalid_subjects.append(grade_subject)
#     return invalid_subjects