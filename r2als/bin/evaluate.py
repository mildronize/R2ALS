#!/usr/bin/env python
__author__ = 'mildronize'

import profile
import os
import csv
from r2als.libs.logs import Log

from r2als import models
from r2als import config
from r2als.engines.processor import Processor
from r2als.engines.filter import Filter

import sys
l=Log("bin/evaluate").getLogger()

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

    # MAX_SUBJECT_PER_SEMESTER
    msps = [
            {'tag':'calculation','value':2},
            {'tag':'english','value':1},
            {'tag':'physic-edu','value':1},
            {'tag':'network','value':1},
            {'tag':'experiment','value':2},
            {'tag':'algorithm','value':1},
            {'tag':'programming','value':1}
        ]

    output_path = 'data/output/'
    output_test_case_path = output_path + test_case_name + '/'
    if not os.path.exists(output_test_case_path):
        os.makedirs(output_test_case_path)

    fieldnames = ['Seed']
    fieldnames+= ['num_iteration','num_cant_find','num_validate_fail','num_add_tabu_fail','num_equal_best']
    fieldnames.append('[Avg]graduate_semester')
    for item in msps:
        fieldnames.append("[Avg]"+item['tag']+" <= " + str(item['value']))
    fieldnames.append('[FailR]graduate_semester')
    for item in msps:
        fieldnames.append("[FailR]"+item['tag']+" <= " + str(item['value']))

    average_overall = ['AVG']
    sum_overall = ['SUM']
    for item in range(1, len(fieldnames)):
        average_overall.append(0)
        sum_overall.append(0)

    num_seed = 1


    with open(output_path+test_case_name+'.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(fieldnames)
        for seed in range(num_seed):
            seed = 37
            p = Processor(member=member,
                          tabu_size=20,
                          target_num_solution=100,
                          seed=seed)
            solutions = p.start()
            filter = Filter(out_path=output_test_case_path,
                            solutions=solutions,
                            max_subject_per_semester=msps,
                            extras=p.conclusion_list(),
                            seed=seed)
            filter.start()
            t = []
            t.append(seed)
            t+= [p.num_iteration,
                 p.num_nsg_fail/p.num_iteration*100,
                 p.num_validate_fail/p.num_iteration*100,
                 p.num_add_tabu_fail/p.num_iteration*100,
                 p.num_equal_best/p.num_iteration*100]
            for i in range(1, len(filter.averages)):
                t.append(filter.averages[i])
            for i in range(1, len(filter.fail_rate)):
                t.append(filter.fail_rate[i])

            l.info(len(t))
            l.info(len(sum_overall))
            for i in range(1, len(average_overall)):
                sum_overall[i] += t[i]
            spamwriter.writerow(t)
        # find average overall
        for i in range(1, len(average_overall)):
            average_overall[i] = sum_overall[i]/num_seed
        spamwriter.writerow(average_overall)



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