import math

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
# function for debugging
def extract_grade_subject(grade_subject):
    return "%s/%s: %s(%s)" % (grade_subject.year, grade_subject.semester, grade_subject.subject.short_name, grade_subject.grade)