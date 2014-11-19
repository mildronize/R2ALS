#!/usr/bin/env python
import pprint
import json

from r2als import models
from r2als import config
from r2als.libs.solutions import InitialSolution
from r2als.libs.export_json import ExportJson
from r2als.libs.export_jointjs import ExportJointjs
# pp = pprint.PrettyPrinter(indent=4)


if __name__ == '__main__':
    # for test
    configuration = config.Configurator(config.root_path + 'development.ini')
    configuration.set('mongodb.is_drop_database', False)
    models.initial(configuration.settings)

    member = models.Member.objects(member_id = '5710110997').first()
    if member is None:
        print('Not found the member')
        exit()

    mSemesters = InitialSolution(member).start()

    json_obj = ExportJson(member, mSemesters).get()
    jointjs_json = ExportJointjs(json_obj).get()

    file = open(config.root_path+'/r2als/interface/joint_semesters.json', 'w')
    # pp = pprint.PrettyPrinter(stream=file,indent=4)
    # pp.pprint(jointjs_json)
    file.write(json.dumps(jointjs_json))
    file.close()
