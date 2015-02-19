# checklist of criteria will be checked
# return true or false

__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als.libs.validators import *

l = Log('Validator').getLogger()

AVAILABLE_VALIDATOR = ['prerequisite_check','grade_subject_format','grade_subject_in_curriculum']

def validator(solution ,checklist):
    count = 0
    if checklist[0] == '*':
        validators = AVAILABLE_VALIDATOR
    else:
        validators = checklist
    for validator in validators:
        if validator == AVAILABLE_VALIDATOR[0]:
            result = prerequisite_check(solution=solution)
            if result: count += 1
            _print_result(validator, result)
        if validator == AVAILABLE_VALIDATOR[1]:
            result = grade_subject_format(solution=solution)
            if result: count += 1
            _print_result(validator, result)
        if validator == AVAILABLE_VALIDATOR[2]:
            result = grade_subject_in_curriculum(solution=solution)
            if result: count += 1
            _print_result(validator, result)
    if count == len(validators):
        return True
    return False

def _print_result(validator_string, result):
    if result:
        l.info("%s\t\t%s" % (validator_string, "PASS"))
    else:
        l.error("%s\t\t%s" % (validator_string, "FAIL"))

