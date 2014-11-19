import unittest
from r2als import models

class ExportsTest(unittest.TestCase):

    # tests class SemesterIndex

    def setUp(self):

        from r2als import config

        configuration = config.Configurator(config.root_path + 'development.ini')
        configuration.set('mongodb.is_drop_database', False)
        models.initial(configuration.settings)

        self.file = open(config.root_path+'/r2als/interface/initial_solotion.json', 'w')

    def tearDown(self):
        self.file.close()

    def test_ExportJointjs(self):
        import json
        from r2als.libs.solutions import InitialSolution
        from r2als.libs.exports import ExportJson, ExportJointjs

        member = models.Member.objects(member_id = '5710110997').first()
        if member is None:
            print('Not found the member')
            exit()

        semesterList = InitialSolution(member).start()
        mSemesters = semesterList.semesters

        json_obj = ExportJson(member, mSemesters).get()
        jointjs_json = ExportJointjs(json_obj).get()

        self.file.write(json.dumps(jointjs_json))

        self.assertNotEqual(jointjs_json, None)
