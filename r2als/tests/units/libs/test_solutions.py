import unittest

class SolutionsTest(unittest.TestCase):

    # test class InitialSolution
    def test_initialEmptySemester(self):
        from r2als.scripts import initial_db
        from r2als.libs.solutions import InitialSolution

        # initial db for testing
        initial_db.main(True, 'coe_2553_curriculum.csv')






    # InitialSolution
