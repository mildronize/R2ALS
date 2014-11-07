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