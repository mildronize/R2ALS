import unittest



class SimpleTest(unittest.TestCase):
    def test_one_plus_one_should_be_two(self):
        self.assertEqual(1+1,2)

    '''def test_initial_db(self):
        from r2als import models
        settings = {'mongodb.db_name':'r2alsdb','mongodb.host':'localhost'}
        self.assertRaises(Exception, models.initial(settings))

    '''
    # def test_add_curriculum(self):
    #     from r2als import models
    #     settings = {'mongodb.db_name':'r2alsdb_test','mongodb.host':'localhost'}
    #     models.initial(settings)
    #     c = models.Curriculum(faculty='Eng',department='CoE',year=2553)
    #     c.save()
    #     c.reload()
    #     self.assertNotEqual(c.id,None)
    #     self.assertEqual(c.faculty,'Eng')
    #     self.assertEqual(c.department,'CoE')
    #     self.assertEqual(c.year,2553)
    #     c.delete()
