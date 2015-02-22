__author__ = 'mildronize'
from r2als.libs.functions import *
from r2als.libs.rules import Rule

# grade_subject must correct in the curriculum

def get_available_semesters(solution, grade_subject):
    lists = []
    l.info(extract_grade_subject(grade_subject))
    si = SemesterIndex(solution.member.curriculum.num_semester)
    rule = Rule(solution.member)
    for semester_id in range(solution.member.num_studied_semester_id, len(solution.semesters)):
        if grade_subject.semester != si.toSemester(semester_id):
            continue
        if semester_id == si.get(grade_subject.year, grade_subject.semester):
            continue
        if solution.semesters[semester_id].calculate_total_credit() + grade_subject.subject.credit > rule.calculate_maximum_credit(semester_id):
            continue
        lists.append(semester_id)
    return lists