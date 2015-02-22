__author__ = 'mildronize'

import unittest
from r2als import models

class TabuHandlerTest(unittest.TestCase):

    def setUp(self):

        from r2als import config
        from r2als.libs.solutions import InitialSolution

        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)
        self.member = models.Member.objects(member_id = '5710110997').first()
        if self.member is None:
            print('Not found the member')
            exit()

        self.solution = InitialSolution(self.member).start()

    # def tearDown(self):
        # self.file.close()

    def __create_empty_solution(self):
        solution = models.Solution()
        solution.member = self.member
        return solution
    # Functional Test
    def test_add_next_solution(self):

        from r2als.engines.tabu_manager import TabuManager
        # == test Normal case
        tabu_handler = TabuManager(10)
        self.assertEqual(tabu_handler.add_next_solution(self.solution), True)
        # Duplicate solution
        self.assertEqual(tabu_handler.add_next_solution(self.solution), False)
        # Empty solution
        self.assertEqual(tabu_handler.add_next_solution(self.__create_empty_solution()), True)
        # == test Full tabu list case
        tabu_handler = TabuManager(1)
        self.assertEqual(tabu_handler.add_next_solution(self.solution), True)
        # Empty solution
        self.assertEqual(tabu_handler.add_next_solution(self.__create_empty_solution()), True)






