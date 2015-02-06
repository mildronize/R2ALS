# checklist of criteria will be checked
# return true or false

__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als.libs.validators import *

l = Log('Validator').getLogger()

AVAILABLE_VALIDATOR = ['prerequisite_check']

def validator(solution ,checklist):
    count = 0
    if checklist[0] == '*':
        validators = AVAILABLE_VALIDATOR
    else:
        validators = checklist
    for validator in validators:
        if validator == AVAILABLE_VALIDATOR[0]:
            result = prerequisite_check(solution)
            if result: count += 1
            _print_result(validator, result)
    if count == len(checklist):
        return True
    return False

def _print_result(validator_string, result):
    if result: result_msg = "PASS"
    else: result_msg = "FAIL"
    l.info("%s\t\t%s" % (validator_string, result_msg ))
