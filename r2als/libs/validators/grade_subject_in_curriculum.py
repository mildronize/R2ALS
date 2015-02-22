__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als import models
from r2als.libs.functions import *
# from r2als.libs.available_semesters import get_available_semesters
l = Log('grade_subject_in_curriculum').getLogger()

def can_enroll(solution, correct_semester, grade_subject):
    si = SemesterIndex(solution.member.curriculum.num_semester)
    semester_id = si.get(grade_subject.year, grade_subject.semester)
    if grade_subject.subject.isSpecific is False:
        return True
    if grade_subject.semester == correct_semester.semester:
        return True
    return False

def is_correct_semester(solution, grade_subject, allow_enroll_cross_subject_group=True):
    if allow_enroll_cross_subject_group:
        subject_groups = models.SubjectGroup.objects(subject=grade_subject.subject,
                                                     curriculum=solution.member.curriculum)
        check = False
        for subject_group in subject_groups:
            if can_enroll(solution, subject_group, grade_subject):
                check = True
                break
        if check is False:
            for subject_group in subject_groups:
                l.error("Because %s is not in correct semester(%d/%d)" % (extract_grade_subject(grade_subject),subject_group.year , subject_group.semester) )
            return False
    else:
        subject_group = models.SubjectGroup.objects(subject=grade_subject.subject,
                                                    curriculum=solution.member.curriculum,
                                                    name=solution.member.subject_group).first()
        if not can_enroll(solution, subject_group, grade_subject):
            l.error("Because %s is not in correct semester(%d/%d)" % (extract_grade_subject(grade_subject),subject_group.year , subject_group.semester) )
            return False
    return True

def grade_subject_in_curriculum(solution, allow_enroll_cross_subject_group=True):
    for semester_id in range(solution.member.num_studied_semester_id,len(solution.semesters)):
        semester = solution.semesters[semester_id]
        for grade_subject in semester.subjects:
            if not is_correct_semester(solution, grade_subject, allow_enroll_cross_subject_group):
                return False
    return True
