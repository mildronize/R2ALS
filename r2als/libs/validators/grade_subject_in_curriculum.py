__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als import models
from r2als.libs.functions import extract_grade_subject
l = Log('grade_subject_in_curriculum').getLogger()

def grade_subject_in_curriculum(solution):
    for semester in solution.semesters:
        for grade_subject in semester.subjects:
            subject_group = models.SubjectGroup.objects(subject=grade_subject.subject,
                                                        curriculum=solution.member.curriculum,
                                                        name=solution.member.subject_group).first()
            if semester.year != subject_group.year or semester.semester != subject_group.semester:
                l.error("Because %s is not in correct semester(%d/%d)" % (extract_grade_subject(grade_subject),subject_group.year , subject_group.semester) )
                return False
    return True
