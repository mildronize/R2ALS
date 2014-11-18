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

    def compare_SemesterId(self, semester_id_1, semester_id_2):
        if semester_id_1.year > semester_id_2.year:
            return 1
        elif semester_id_1.year < semester_id_2.year:
            return -1
        else:
            # equal
            if semester_id_1.semester > semester_id_2.semester:
                return 1
            elif semester_id_1.semester < semester_id_2.semester:
                return -1
            else:
                return 0
