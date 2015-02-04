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
        # print(p.hashSolution([0,1,2,3,4,5,6,7,8,9]))
        # for sha 256
        self.assertEqual(p.hashSolution([0,1,2,3,4,5,6,7,8,9]),'f4972c7d08e0c80337aff8d177d66062c2be8a625f71e02b927f3c9aa3a2f48e')
        # for sha 512
        #self.assertEqual(p.hashSolution([0,1,2,3,4,5,6,7,8,9]),'8b0ee12df74c1f9ae763d404c3821eb7a7689fa9f78b9c97a867de616e30b4af40b706d241d2b46176745758108c35abd8d204806710ae3a0924d8216aa83540')

    def test_convertList2String(self):
        from r2als import processor
        p = processor.Processor()
        self.assertEqual(p.convertList2String([0,1,2,3,4,5,6,7,8,9]),b'0,1,2,3,4,5,6,7,8,9')

    # def test_hasTabuLists(self):
    #     from r2als import processor
    #     p = processor.Processor()
    #

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
