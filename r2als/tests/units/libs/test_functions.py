import unittest

class FunctionsTest(unittest.TestCase):

    # tests class SemesterIndex

    def test_get(self):
        from r2als.libs.functions import SemesterIndex
        semesterIndex = SemesterIndex(3)
        self.assertEqual(semesterIndex.get(1,1),0)
        self.assertEqual(semesterIndex.get(1,2),1)
        self.assertEqual(semesterIndex.get(1,3),2)
        self.assertEqual(semesterIndex.get(2,1),3)
        self.assertEqual(semesterIndex.get(2,2),4)
        self.assertEqual(semesterIndex.get(2,3),5)
        self.assertEqual(semesterIndex.get(3,1),6)
        self.assertEqual(semesterIndex.get(3,2),7)
        self.assertEqual(semesterIndex.get(3,3),8)
        self.assertEqual(semesterIndex.get(4,1),9)
        self.assertEqual(semesterIndex.get(4,2),10)
        self.assertEqual(semesterIndex.get(4,3),11)
        self.assertEqual(semesterIndex.get(5,1),12)
        self.assertEqual(semesterIndex.get(5,2),13)
        self.assertEqual(semesterIndex.get(5,3),14)
        self.assertEqual(semesterIndex.get(6,1),15)
        self.assertEqual(semesterIndex.get(6,2),16)
        self.assertEqual(semesterIndex.get(6,3),17)

    def test_toYear(self):
        from r2als.libs.functions import SemesterIndex
        semesterIndex = SemesterIndex(3)
        self.assertEqual(semesterIndex.toYear(0),1)
        self.assertEqual(semesterIndex.toYear(1),1)
        self.assertEqual(semesterIndex.toYear(2),1)
        self.assertEqual(semesterIndex.toYear(3),2)
        self.assertEqual(semesterIndex.toYear(4),2)
        self.assertEqual(semesterIndex.toYear(5),2)
        self.assertEqual(semesterIndex.toYear(6),3)
        self.assertEqual(semesterIndex.toYear(7),3)
        self.assertEqual(semesterIndex.toYear(8),3)
        self.assertEqual(semesterIndex.toYear(9),4)
        self.assertEqual(semesterIndex.toYear(10),4)
        self.assertEqual(semesterIndex.toYear(11),4)
        self.assertEqual(semesterIndex.toYear(12),5)
        self.assertEqual(semesterIndex.toYear(13),5)
        self.assertEqual(semesterIndex.toYear(14),5)
        self.assertEqual(semesterIndex.toYear(15),6)
        self.assertEqual(semesterIndex.toYear(16),6)
        self.assertEqual(semesterIndex.toYear(17),6)

    def test_toSemester(self):
        from r2als.libs.functions import SemesterIndex
        semesterIndex = SemesterIndex(3)
        self.assertEqual(semesterIndex.toSemester(0),1)
        self.assertEqual(semesterIndex.toSemester(1),2)
        self.assertEqual(semesterIndex.toSemester(2),3)
        self.assertEqual(semesterIndex.toSemester(3),1)
        self.assertEqual(semesterIndex.toSemester(4),2)
        self.assertEqual(semesterIndex.toSemester(5),3)
        self.assertEqual(semesterIndex.toSemester(6),1)
        self.assertEqual(semesterIndex.toSemester(7),2)
        self.assertEqual(semesterIndex.toSemester(8),3)
        self.assertEqual(semesterIndex.toSemester(9),1)
        self.assertEqual(semesterIndex.toSemester(10),2)
        self.assertEqual(semesterIndex.toSemester(11),3)
        self.assertEqual(semesterIndex.toSemester(12),1)
        self.assertEqual(semesterIndex.toSemester(13),2)
        self.assertEqual(semesterIndex.toSemester(14),3)
        self.assertEqual(semesterIndex.toSemester(15),1)
        self.assertEqual(semesterIndex.toSemester(16),2)
        self.assertEqual(semesterIndex.toSemester(17),3)

    def test_compare_semester(self):
        from r2als.libs.functions import SemesterIndex
        semesterIndex = SemesterIndex(3)
        self.assertEqual(semesterIndex.compare_semester(1,1,1,1), 0)
        self.assertEqual(semesterIndex.compare_semester(2,2,2,2), 0)
        self.assertEqual(semesterIndex.compare_semester(2,1,1,1), 1)
        self.assertEqual(semesterIndex.compare_semester(1,1,2,1), -1)
        self.assertEqual(semesterIndex.compare_semester(2,1,2,2), -1)
        self.assertEqual(semesterIndex.compare_semester(3,1,2,2), 1)
        self.assertEqual(semesterIndex.compare_semester(3,2,3,1), 1)
