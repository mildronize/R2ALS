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


    # InitialSolution
