import unittest



class ScoringTest(unittest.TestCase):

    def test_scoring(self):
        from r2als import scoring
        s = scoring.Scoring()
        self.assertEqual(s.calculate(),0)
