__author__ = 'mildronize'

import unittest
from r2als import models

class ValidatorTest(unittest.TestCase):

    def setUp(self):

        from r2als import config
        from r2als.libs.solutions import InitialSolution

        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)
        member = models.Member.objects(member_id = '5710110997').first()
        if member is None:
            print('Not found the member')
            exit()

        self.solution = InitialSolution(member).start()

    # def tearDown(self):
        # self.file.close()

    # Functional Test
    def test_validator(self):
        from r2als.engines.validator import validator

        self.assertEqual(validator(self.solution, ['prerequisite_check']), True)
