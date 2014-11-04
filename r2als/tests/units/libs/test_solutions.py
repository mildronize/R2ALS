import unittest

class SolutionsTest(unittest.TestCase):


    def test_toSemesterIndex(self):
        from r2als.libs import solutions
        self.assertEqual(solutions.toSemesterIndex(1,1),0)
        self.assertEqual(solutions.toSemesterIndex(1,2),1)
        self.assertEqual(solutions.toSemesterIndex(1,3),2)
        self.assertEqual(solutions.toSemesterIndex(2,1),3)
        self.assertEqual(solutions.toSemesterIndex(2,2),4)
        self.assertEqual(solutions.toSemesterIndex(2,3),5)
        self.assertEqual(solutions.toSemesterIndex(3,1),6)
        self.assertEqual(solutions.toSemesterIndex(3,2),7)
        self.assertEqual(solutions.toSemesterIndex(3,3),8)
        self.assertEqual(solutions.toSemesterIndex(4,1),9)
        self.assertEqual(solutions.toSemesterIndex(4,2),10)
        self.assertEqual(solutions.toSemesterIndex(4,3),11)

    def test_toYear(self):
        from r2als.libs import solutions
        self.assertEqual(solutions.toYear(0),1)
        self.assertEqual(solutions.toYear(1),1)
        self.assertEqual(solutions.toYear(2),1)
        self.assertEqual(solutions.toYear(3),2)
        self.assertEqual(solutions.toYear(4),2)
        self.assertEqual(solutions.toYear(5),2)
        self.assertEqual(solutions.toYear(6),3)
        self.assertEqual(solutions.toYear(7),3)
        self.assertEqual(solutions.toYear(8),3)
        self.assertEqual(solutions.toYear(9),4)
        self.assertEqual(solutions.toYear(10),4)
        self.assertEqual(solutions.toYear(11),4)

    def test_toSemester(self):
        from r2als.libs import solutions
        self.assertEqual(solutions.toSemester(0),1)
        self.assertEqual(solutions.toSemester(1),2)
        self.assertEqual(solutions.toSemester(2),3)
        self.assertEqual(solutions.toSemester(3),1)
        self.assertEqual(solutions.toSemester(4),2)
        self.assertEqual(solutions.toSemester(5),3)
        self.assertEqual(solutions.toSemester(6),1)
        self.assertEqual(solutions.toSemester(7),2)
        self.assertEqual(solutions.toSemester(8),3)
        self.assertEqual(solutions.toSemester(9),1)
        self.assertEqual(solutions.toSemester(10),2)
        self.assertEqual(solutions.toSemester(11),3)


    # InitialSolution
