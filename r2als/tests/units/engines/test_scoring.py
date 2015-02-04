import unittest



class ScoringTest(unittest.TestCase):

    #todo: Test this module!
    def test_scoring(self):
        from r2als import scoring
        self.assertEqual(scoring.calculate([0,1,2,3,4,5,6,7,8,9]),9)
        self.assertEqual(scoring.calculate([9,8,7,6,5,4,3,2,1,0]),0)
