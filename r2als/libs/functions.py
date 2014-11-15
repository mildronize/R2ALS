import math

class SemesterIndex:

    def __init__(self, num_semester):
        self.num_semester = num_semester

    # convert Year & Semester to SemesterIndex
    def get(self, year, semester):
        return ((year-1) * self.num_semester + semester) - 1

    # convert SemesterIndex to Year
    def toYear(self, semesterIndex):
        return math.ceil((semesterIndex + 1) / self.num_semester)

    # convert SemesterIndex to Semester
    def toSemester(self, semesterIndex):
        return semesterIndex + 4 - (3 * self.toYear(semesterIndex))

    # def compare semester 
