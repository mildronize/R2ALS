import unittest



class ProcessorTest(unittest.TestCase):

    # def test_processor(self):
    #     from r2als import processor
    #     p = processor.Processor()
    #     self.assertEqual(p.start(),None)

    def test_hashSolution(self):
        from r2als import processor
        p = processor.Processor()
        # self.assertEqual(p.hashSolution(b'Hello World'),'2c74fd17edafd80e8447b0d46741ee243b7eb74dd2149a0ab1b9246fb30382f27e853d8585719e0e67cbda0daa8f51671064615d645ae27acb15bfb1447f459b')
        self.assertEqual(p.hashSolution([0,1,2,3,4,5,6,7,8,9]),None)


    # def test_one_plus_one_should_be_two(self):
    #     self.assertEqual(1+1,2)

    # def test_initial_db(self):
    #     from r2als import models
    #     settings = {'mongodb.db_name':'r2alsdb','mongodb.host':'localhost'}
    #     self.assertRaises(Exception, models.initial(settings))


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
