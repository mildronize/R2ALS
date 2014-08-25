'''
initialize.py
Description#   Initialize a database and test case
Developer#     Thada Wangthammang
'''
import os
import sys
import pymongo

from .. import models

def usage(argv):
    cmd = os.path.basename(argv[0])
    # print('usage: %s <config_uri>\n'
    #       '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    # if len(argv) != 2:
    #     usage(argv)
    # config_uri = argv[1]
    # setup_logging(config_uri)
    # settings = get_appsettings(config_uri)

    #models.initial(settings)

    print ("Initial a database")

    print ("initial default categories")
    default_categories = ['lecture', 'lab','project']
    for category in default_categories:
        category_tmp = models.Category.objects(name=category).first()
        if not category_tmp:
            category_tmp = models.Category()
            category_tmp.name = category
            category_tmp.save()

    'Initial test cases'
