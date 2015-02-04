import unittest
from r2als import models

def gs(year, semester, grade):
    #create grade subject
    if grade == '': return models.GradeSubject(year = year, semester = semester)
    else:
        grade = models.Grade.objects(name = grade).first()
        if grade is not None:
            return models.GradeSubject(grade = grade,
                                       year = year, semester = semester)
        else: print('Not found the grade')

class PrerequisiteTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.member = models.Member.objects(member_id = '5710110997').first()

    def test_canEnrolled(self):
        from r2als.libs.prerequisites import Prerequisite as P
        self.assertEqual(P(gs(0,0,''), gs(0,0,''), self.member).canEnrolled(), False)

class StudiedPrerequisiteTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.member = models.Member.objects(member_id = '5710110997').first()

    def test_canEnrolled(self):
        from r2als.libs.prerequisites import StudiedPrerequisite as SP
        # check all credit grade
        self.assertEqual(SP(gs(1,1,'W'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(SP(gs(1,1,'E'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'D'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'D+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'C'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'C+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'B'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'B+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'A'), gs(1,2,''), self.member).canEnrolled(), True)
        #check all audit grade
        self.assertEqual(SP(gs(1,1,'S'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(SP(gs(1,1,'U'), gs(1,2,''), self.member).canEnrolled(), True)
        # check all semster
        self.assertEqual(SP(gs(1,2,'C'), gs(1,1,''), self.member).canEnrolled(), False)
        self.assertEqual(SP(gs(1,1,'C'), gs(1,1,''), self.member).canEnrolled(), False)
        self.assertEqual(SP(gs(2,1,'C'), gs(1,1,''), self.member).canEnrolled(), False)

class PassedPrerequisiteTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.member = models.Member.objects(member_id = '5710110997').first()

    def test_canEnrolled(self):
        from r2als.libs.prerequisites import PassedPrerequisite as PP
        # check all credit grade
        self.assertEqual(PP(gs(1,1,'W'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(PP(gs(1,1,'E'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(PP(gs(1,1,'D'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'D+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'C'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'C+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'B'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'B+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'A'), gs(1,2,''), self.member).canEnrolled(), True)
        #check all audit grade
        self.assertEqual(PP(gs(1,1,'S'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(PP(gs(1,1,'U'), gs(1,2,''), self.member).canEnrolled(), False)
        # check all semster
        self.assertEqual(PP(gs(1,2,'C'), gs(1,1,''), self.member).canEnrolled(), False)
        self.assertEqual(PP(gs(1,1,'C'), gs(1,1,''), self.member).canEnrolled(), False)
        self.assertEqual(PP(gs(2,1,'C'), gs(1,1,''), self.member).canEnrolled(), False)

class CorequisiteTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.member = models.Member.objects(member_id = '5710110997').first()

    def test_canEnrolled(self):
        from r2als.libs.prerequisites import Corequisite as CR
        # check all credit grade
        self.assertEqual(CR(gs(1,1,'W'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CR(gs(1,1,'E'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'D'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'D+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'C'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'C+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'B'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'B+'),gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'A'), gs(1,2,''), self.member).canEnrolled(), True)
        #check all audit grade
        self.assertEqual(CR(gs(1,1,'S'), gs(1,2,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(1,1,'U'), gs(1,2,''), self.member).canEnrolled(), True)
        # check all semster
        self.assertEqual(CR(gs(1,2,'C'), gs(1,1,''), self.member).canEnrolled(), False)
        self.assertEqual(CR(gs(1,1,'C'), gs(1,1,''), self.member).canEnrolled(), True)
        self.assertEqual(CR(gs(2,1,'C'), gs(1,1,''), self.member).canEnrolled(), False)

class CocurrentTest(unittest.TestCase):

    def setUp(self):
        from r2als import config
        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.member = models.Member.objects(member_id = '5710110997').first()

    def test_canEnrolled(self):
        from r2als.libs.prerequisites import Cocurrent as CC
        # check all credit grade
        self.assertEqual(CC(gs(1,1,'W'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'E'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'D'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'D+'),gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'C'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'C+'),gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'B'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'B+'),gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'A'), gs(1,2,''), self.member).canEnrolled(), False)
        #check all audit grade
        self.assertEqual(CC(gs(1,1,'S'), gs(1,2,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(1,1,'U'), gs(1,2,''), self.member).canEnrolled(), False)
        # check all semster
        self.assertEqual(CC(gs(1,2,'C'), gs(1,1,''), self.member).canEnrolled(), False)
        self.assertEqual(CC(gs(2,1,'C'), gs(1,1,''), self.member).canEnrolled(), False)

        self.assertEqual(CC(gs(1,1,'C'), gs(1,1,''), self.member).canEnrolled(), True)
        self.assertEqual(CC(gs(2,1,'C'), gs(2,1,''), self.member).canEnrolled(), True)
