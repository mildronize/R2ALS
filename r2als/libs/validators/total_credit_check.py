__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als.libs.functions import *
l = Log('total_credit_check').getLogger()

def total_credit_check(solution):
    for semester in solution.semesters:
        if semester.total_credit != semester.calculate_total_credit():
            return False
        # l.info(semester.total_credit)
    return True
