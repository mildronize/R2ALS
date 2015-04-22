#!/usr/bin/env python
import profile
import os
import csv
from r2als.libs.logs import Log

from r2als import models
from r2als import config
from r2als.engines.processor import Processor
from r2als.engines.filter import Filter

import sys
l=Log("bin/r2als").getLogger()

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <test_case_name>\n'
          '(example: "%s development.ini testcase1")' % (cmd, cmd))
    sys.exit(1)

def main():
#if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv)
        sys.exit()

    test_case_name = sys.argv[2]
    config_uri = sys.argv[1]

    configuration = config.Configurator(config.root_path + config_uri)
    models.initial(configuration.settings)

    # profile.run("print('555')")
    start(test_case_name)

def start(test_case_name):
    member = models.Member.objects(member_id=test_case_name).first()
    if member is None:
        l.error('No have '+ test_case_name + ' in db!')
        exit(0)

    seed = 37
    p = Processor(member=member,
                  tabu_size=20,
                  target_num_solution=20,
                  seed=seed)
    solutions = p.start()
    # filter = Filter(out_path=output_test_case_path,
    #                 solutions=solutions,
    #                 max_subject_per_semester=msps,
    #                 extras=p.conclusion_list(),
    #                 seed=seed)
    # filter.start()



    #settings = {'mongodb.db_name':'r2alsdb','mongodb.host':'localhost'}
    # if len(sys.argv) < 2:
    #     #sys.stderr.write( "Use: " + sys.argv[0] + " configure_file")
    #     sys.exit(errno.EINVAL)pip

    # for i in range(10):
    #     tabuSize = i*10
    #     print("#"*30)
    #     print("Tabu Size: "+ str(tabuSize))
    #     p = processor.Processor(tabuSize)
    #     profile.run('p.start()')
    #     print("#"*30)
    #     input("press enter")
    # p = processor.Processor(10)
    # profile.run('p.start()')
    # p.start()

    # print("test")