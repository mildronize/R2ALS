__author__ = 'mildronize'

import unittest
from r2als import models

class MoveWholeChainTest(unittest.TestCase):

    def setUp(self):

        from r2als import config

        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.file = open(config.root_path+'/r2als/interface/processing_solution.json', 'w')

        import json
        from r2als.libs.solutions import InitialSolution
        from r2als.libs.exports import ExportJson, ExportJointjs
        from r2als.libs import next_solution_methods

        member = models.Member.objects(member_id = '5710110997').first()
        if member is None:
            print('Not found the member')
            exit()

        semesterList = InitialSolution(member).start()
        mSemesters = next_solution_methods.MoveWholeChain(semesterList).start()

        json_obj = ExportJson(member, mSemesters).get()
        jointjs_json = ExportJointjs(json_obj).get()

        self.file.write(json.dumps(jointjs_json))

    def tearDown(self):
        self.file.close()

    def test_MoveWholeChain(self):
        self.assertEqual(True,True)