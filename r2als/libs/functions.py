import math
from r2als.libs.logs import Log
l = Log("functions").getLogger()

class SemesterIndex:

    def __init__(self, num_semester = 0):
        self.num_semester = num_semester

    # convert Year & Semester to SemesterIndex
    def get(self, year, semester):
        return ((year-1) * self.num_semester + semester) - 1

    # convert SemesterIndex to Year
    def toYear(self, semester_index):
        return math.ceil((semester_index + 1) / self.num_semester)

    # convert SemesterIndex to Semester
    def toSemester(self, semester_index):
        return semester_index + 4 - (3 * self.toYear(semester_index))

    def count_specific_semesters(self, semester_index, specific_semesters=[]):
        count = 0
        for specific_semester in specific_semesters:
            count += self.count_specific_semester(semester_index, specific_semester)
        return count

    def count_specific_semester(self, semester_index, specific_semester):
        count = 0
        for i in range(semester_index + 1):
            if self.toSemester(specific_semester) == specific_semester:
                count +=1
        return count


    def compare_semester(self, year1, semester1, year2, semester2):
        if year1 > year2:
            return 1
        elif year1 < year2:
            return -1
        else:
            # equal
            if semester1 > semester2:
                return 1
            elif semester1 < semester2:
                return -1
            else:
                return 0

def response_json(data, message_type="success", message=""):
    result = {
        'type': message_type,
        'data': data
    }
    message_type_available = ['success','error','warning']
    if message_type in message_type_available:
        if message_type == message_type_available[0]:
            return result
        else:
            result['message'] = message
            return result
    else:
        l.error("Not found response_json message_type")



# function for debugging
def extract_grade_subject(grade_subject):
    if grade_subject is None:
        return "Grade subject is None"
    elif grade_subject.grade is None:
        return "%s/%s: %s(%s)" % (grade_subject.year, grade_subject.semester, grade_subject.subject.short_name, grade_subject.grade)
    return "%s/%s: %s(%s)" % (grade_subject.year, grade_subject.semester, grade_subject.subject.short_name, grade_subject.grade.name)

def extract_solution(solution, semester_id):
    si = SemesterIndex(solution.member.curriculum.num_semester)
    tmp = str(si.toYear(semester_id))+"/"+str(si.toSemester(semester_id))
    tmp += " [ "
    for grade_subject in solution.semesters[semester_id].subjects:
        tmp += '"'+grade_subject.subject.short_name+'", '
    tmp = tmp[:len(tmp)-2]
    tmp += " ]"
    return tmp

