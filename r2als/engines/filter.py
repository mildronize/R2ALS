__author__ = 'mildronize'
# Zero score is best
# Much score is worst

import csv
from r2als.libs.functions import SemesterIndex
from r2als.libs.logs import Log

l = Log('Filter').getLogger()

class Filter:

    def __init__(self, out_path, solutions, max_subject_per_semester, extras=[], seed=None):
        print("running Filter")
        self.solutions = solutions
        self.extras = extras
        self.out_path = out_path
        self.seed = seed
        self.si = SemesterIndex(solutions[0].member.curriculum.num_semester)

        self.EXPECTED_GRADUATE_SEMESTER = self.si.get(5,1)
        # MAX_SUBJECT_PER_SEMESTER
        self.msps = max_subject_per_semester
        # self.si = SemesterIndex(self.member.curriculum.num_semester)

    def start(self):
        l.info("start")
        i = 0
        # t = []
        # for item in self.msps:
        #     t.append(item['tag'])
        # l.info("%s"% list(t))


        for solution in self.solutions:
            solution.scores = self.filter_solution(solution)
            # i+=1
            # l.info("solution %d: %s"% (i,list(solution.scores)))
            # l.info("max-> %d" % self.count_subject_with_tag_per_semester(solution,'calculation')['max'])
            # l.info("max-> %d" % self.count_subject_with_tag_per_semester(solution,'calculation')['max_semester'])
        self._print_to_csv(self.solutions)
        return self.solutions

    def _print_to_csv(self, solutions):
        fieldnames = ['SID','graduate_semester']
        values =['',' <= 5/1']
        for item in self.msps:
            fieldnames.append(item['tag'])
            values.append(" <= " + str(item['value']))
        self.sums = ['Sum']
        self.averages = ['Avg Fail']
        self.pass_rate = ['Pass Rate']
        self.fail_rate = ['Fail Rate']
        self.num_pass = ['Num Pass']
        self.num_fail = ['Num Fail']
        for i in range(1, len(fieldnames)):
            self.sums.append(0)
            self.averages.append(0)
            self.pass_rate.append('')
            self.fail_rate.append('')
            self.num_pass.append(0)
            self.num_fail.append(0)

        with open(self.out_path+'filter-seed-'+str(self.seed)+'.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            spamwriter.writerow(fieldnames)
            spamwriter.writerow(values)
            i = 1
            for solution in solutions:
                spamwriter.writerow([i]+list(solution.scores)+[self.sum_score(list(solution.scores))])
                for score_id,score in enumerate(solution.scores, start=1):
                    self.sums[score_id] += score
                    if score == 0:
                        self.num_pass[score_id] += 1
                    else:
                        self.num_fail[score_id] += 1
                i+=1
            spamwriter.writerow(self.sums)
            # l.info(self.averages)
            # l.info(self.sums)
            for i in range(1, len(self.averages)):
                # l.info(i)
                self.averages[i]= self.sums[i]/len(solutions)
                self.pass_rate[i] = self.num_pass[i]/len(solutions)*100
                self.fail_rate[i] = self.num_fail[i]/len(solutions)*100

            spamwriter.writerow(self.averages)
            spamwriter.writerow(self.num_pass)
            spamwriter.writerow(self.num_fail)
            spamwriter.writerow(self.pass_rate)
            spamwriter.writerow(self.fail_rate)

            spamwriter.writerow(['-'*40])
            spamwriter.writerow(['Conclusion'])
            spamwriter.writerow(['-'*40])
            for extra in self.extras:
                spamwriter.writerow([extra])

    def sum_score(self, scores):
        total = 0
        for score in scores:
            total+=score
        return total

    def scoring_condition(self, a, b, score):
        cmp_value = a - b
        if cmp_value <= 0:
            return 0
        else:
            return cmp_value*score

    def filter_solution(self, solution):
        tmp = []
        tmp.append(self.scoring_condition(len(solution.semesters),
                                          self.EXPECTED_GRADUATE_SEMESTER,
                                          1))
        for item in self.msps:
            tmp.append(self.scoring_condition(self.count_subject_with_tag_per_semester(solution,item['tag'])['max'],
                                              item['value'],
                                              1))


        # if len(solution.semesters) <= self.EXPECTED_GRADUATE_SEMESTER:
        #     tmp.append(1)
        # else:
        #     tmp.append(0)
        #
        # if self.count_subject_with_tag_per_semester(solution,'calculation')['max'] \
        #         <= self.MAX_CALC_SUBJECT_PER_SEMESTER:
        #     tmp.append(1)
        # else:
        #     tmp.append(0)
        #
        # if self.count_subject_with_tag_per_semester(solution,'english')['max'] \
        #         <= self.MAX_CALC_SUBJECT_PER_SEMESTER:
        #     tmp.append(1)
        # else:
        #     tmp.append(0)
        return tmp

    def count_subject_with_tag_per_semester(self, solution, tag_name):
        total = {
            'min': 9999,
            'max': 0
        }
        for semester in solution.semesters:
            num_subjects = 0
            for grade_subject in semester.subjects:
                if tag_name in grade_subject.subject.tags:
                    num_subjects += 1
            if num_subjects < total['min']:
                total['min'] = num_subjects
                total['min_semester'] = self.si.get(semester.year, semester.semester)
            if num_subjects > total['max']:
                total['max'] = num_subjects
                total['max_semester'] = self.si.get(semester.year, semester.semester)
        return total



