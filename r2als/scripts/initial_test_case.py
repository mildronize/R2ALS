'''
initial_test_case
Description#   Initialize test case
Developer#     Thada Wangthammang
'''
__author__ = 'mildronize'
import os
import sys
import json
import pymongo
import pprint
from mongoengine import Q

from r2als import models
from r2als import config
from r2als.scripts.initial_db import add_member
from r2als.libs.logs import Log
def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <test_cases_path>\n'
          '(example: "%s test.ini data/test_cases")' % (cmd, cmd))
    sys.exit(1)

def main():
#if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv)
        sys.exit()

    test_cases_path = sys.argv[2]
    configuration = config.Configurator(sys.argv[1])
    models.initial(configuration.settings)

    for file in get_test_case_files(test_cases_path):
        string_json = open(test_cases_path+"/"+file, 'r').read()
        member_json = json.loads(string_json)
        if 'name' not in member_json['info']:
            member_json['info']['name'] = member_json['info']['member_id']
        # todo: Force first curriculum
        member_json['info']['curriculum'] = models.Curriculum.objects().first()
        print(member_json['info']['curriculum'])
        add_member(member_json)

def get_test_case_files(test_cases_path):
    items =[]
    for file in os.listdir(test_cases_path):
        if file.endswith(".json"):
            items.append(file)
    return items