import pprint

from r2als.libs.logs import Log
from r2als import models
from r2als import config
from r2als.libs.functions import SemesterIndex

l = Log('exports').getLogger()

class ExportJson:

    def __init__(self, solution):
        l.info('hello ExportJson')
        self.member = solution.member
        self.solution = solution
        self.json_object = dict()
        self.si = SemesterIndex(solution.member.curriculum.num_semester)

    def hasPrerequisite(self, gradeSubject):
        if gradeSubject.subject.prerequisites == [] and gradeSubject.subject.reverse_prerequisites == []:
            return False
        return True

    def countPrerequisite(self, gradeSubject):
        return len(gradeSubject.subject.prerequisites)
    def countReverse_prerequisites(self, gradeSubject):
        return len(gradeSubject.subject.reverse_prerequisites)

    def findTotalCredit(self, mSemester):
        total_credit = 0
        for gradeSubject in mSemester.subjects:
            total_credit += gradeSubject.subject.credit
        return total_credit

    def findTotalCreditList(self, mSemesters):
        lists = list()
        for i in range(len(self.solution.semesters)):
            lists.append(self.findTotalCredit(mSemesters[i]))
            # lists.append(0)
        return lists

    def namingSubject(self, mSemesters, cur_year, cur_semester, original_id):
        cmp_semester = self.si.compare_semester(cur_year, cur_semester,
                                                self.member.last_year,
                                                self.member.last_semester)
        if cmp_semester < 0 or cmp_semester == 0:
            # studied semester
            tmp_subject_id = original_id
            last_semester_id = self.si.get(self.member.last_year,
                                           self.member.last_semester)
            for i in range(last_semester_id + 1, len(mSemesters)):
                for gradeSubject in mSemesters[i].subjects:
                    if tmp_subject_id == str(gradeSubject.subject.id):
                        tmp_subject_id += '_old'
                        return tmp_subject_id
        return original_id

    def exportListSubject(self, mSemesters):
        lists = []
        for mSemester in mSemesters:
            year = mSemester.year
            semester = mSemester.semester
            for gradeSubject in mSemester.subjects:
                # if self.hasPrerequisite(gradeSubject):
                subject = dict()
                subject['year'] = year
                subject['semester'] = semester
                subject['id'] = self.namingSubject(mSemesters, year, semester, str(gradeSubject.subject.id))
                subject['name']  = gradeSubject.subject.short_name
                subject['hasPrerequisite'] = self.hasPrerequisite(gradeSubject)
                subject['numPrerequisite'] = self.countPrerequisite(gradeSubject)
                subject['numReverse_prerequisite'] = self.countReverse_prerequisites(gradeSubject)
                subject['credit']  = gradeSubject.subject.credit

                if 'grade' in gradeSubject:
                    subject['grade'] = gradeSubject.grade.name
                lists.append(subject)

        return sorted(lists, key=lambda k: k['hasPrerequisite'], reverse= True)

    def exportListSemester(self, mSemesters):
        lists = []
        for mSemester in mSemesters:
            # year = mSemester.year
            # semester = mSemester.semester
            tmp = dict()
            tmp['year'] = mSemester.year
            tmp['semester'] = mSemester.semester
            tmp['subjects'] = []
            for gradeSubject in mSemester.subjects:
                # if self.hasPrerequisite(gradeSubject):
                subject = dict()
                subject['semesterIndex'] = self.si.get(tmp['year'], tmp['semester'])
                subject['year'] = tmp['year']
                subject['semester'] = tmp['semester']
                subject['id'] = self.namingSubject(mSemesters, tmp['year'], tmp['semester'], str(gradeSubject.subject.id))
                subject['name']  = gradeSubject.subject.short_name
                subject['hasPrerequisite'] = self.hasPrerequisite(gradeSubject)
                subject['numPrerequisite'] = self.countPrerequisite(gradeSubject)
                subject['numReverse_prerequisite'] = self.countReverse_prerequisites(gradeSubject)
                subject['credit']  = gradeSubject.subject.credit

                if 'grade' in gradeSubject:
                    subject['grade'] = gradeSubject.grade.name
                tmp['subjects'].append(subject)
                tmp['subjects'] = sorted(tmp['subjects'], key=lambda k: k['hasPrerequisite'], reverse= True)
            lists.append(tmp)
        return lists

    def exportLink(self, mSemesters):
        lists = []
        for mSemester in mSemesters:
            year = mSemester.year
            semester = mSemester.semester
            for gradeSubject in mSemester.subjects:
                source = gradeSubject.subject.id
                for prerequisite in gradeSubject.subject.prerequisites:
                    link = dict()
                    link['source'] = str(source)
                    link['target'] =  str(prerequisite.subject.id)
                    link['type'] = prerequisite.name
                    lists.append(link)
                    # print(prerequisite.subject.short_name,' --->',gradeSubject.subject.short_name)
        return lists

    def get(self):
        return self.get_subject_list()

    def get_subject_list(self):
        self.json_object['subjects'] = self.exportListSubject(self.solution.semesters)

        self.json_object['links'] = self.exportLink(self.solution.semesters)
        print(len(self.json_object['links']))
        self.json_object['num_semester'] = self.solution.member.curriculum.num_semester

        # plus one year because it is spare semester
        self.json_object['num_year'] = self.member.curriculum.required_num_year + 1

        self.json_object['last_year'] = self.solution.member.last_year
        self.json_object['last_semester'] = self.solution.member.last_semester

        l.info(self.solution.member.name)
        self.json_object['total_credits'] = self.findTotalCreditList(self.solution.semesters)
        return self.json_object

    def get_semester_list(self):
        self.json_object['semesters'] = self.exportListSemester(self.solution.semesters)

        self.json_object['links'] = self.exportLink(self.solution.semesters)

        self.json_object['num_semester'] = self.solution.member.curriculum.num_semester

        # plus one year because it is spare semester
        self.json_object['num_year'] = self.member.curriculum.required_num_year + 1

        self.json_object['last_year'] = self.solution.member.last_year
        self.json_object['last_semester'] = self.solution.member.last_semester

        l.info(self.solution.member.name)
        self.json_object['total_credits'] = self.findTotalCreditList(self.solution.semesters)
        return self.json_object


class ExportJointjs:

    def __init__(self, json_object):
        l.info('hello ExportJointjs')
        self.width = 100
        self.height = 40

        self.offset_start_x = 30 # 50
        self.offset_start_y = 30

        self.offset_width = 50
        self.offset_height = 40

        self.offset_height_non_prereq = 15

        self.jointjs_object = dict()
        self.si = SemesterIndex(json_object['num_semester'])
        self.last_year = json_object['last_year']
        self.last_semester = json_object['last_semester']
        self.list_num_subject = self.initialZeroList(json_object['num_year'], json_object['num_semester'])
        self.jointjs_object['cells'] = self.start(json_object, json_object['num_year'], json_object['num_semester'])

    def initialZeroList(self, num_year, num_semester):
        lists = list()
        for i in range(num_year * num_semester):
            lists.append(0)
        return lists

    def addList_num_subject(self, index, hasPrerequisite =True, offset= 0):
        self.list_num_subject[index] += self.height
        if hasPrerequisite:
            self.list_num_subject[index] += self.offset_height
        else:
            self.list_num_subject[index] += self.offset_height_non_prereq
        self.list_num_subject[index] += offset

    def semesterToCoordinate(self, semesterIndex):
        x = self.offset_start_x + semesterIndex * (self.width + self.offset_width)
        y = self.offset_start_y + self.list_num_subject[semesterIndex]
        # y = self.offset_start_y + self.list_num_subject[semesterIndex] * (self.height+ self.offset_height)
        return {
            'x': x,
            'y': y,
        }

    def createSemesterLabel(self, semesterIndex, total_credit):
        year = self.si.toYear(semesterIndex)
        semester = self.si.toSemester(semesterIndex)
        coordinate = self.semesterToCoordinate(semesterIndex)
        x = coordinate['x']
        y = coordinate['y']
        semester_id = 'semester-label-'+str(year)+'-'+str(semester)
        name = str(year)+' / '+str(semester) + '('+str(total_credit)+')'
        return {
            "id": semester_id,
            "type": "basic.Rect",
            "attrs": { "text": {
                         "text": name,
                         "font-size": 20,
                         'font-weight': 'bold'
                        },
                        "rect" : {
                         "stroke-width": 1
                        }
                     },
            "position":{"x": x,"y": y},
            "size":{"width": self.width,"height":self.height},
            "angle": 0,
            "z": 1
        }

    def createSemesterLabelList(self, num_year, num_semester, total_credits):
        lists = list()
        for i in range(num_year * num_semester):
            lists.append(self.createSemesterLabel(i, total_credits[i]))
            self.addList_num_subject(i, True, 0)
        return lists

    def createSubject(self, obj):
        semesterIndex = self.si.get(obj['year'], obj['semester'])

        subjec_id = obj['id']

        name = obj['name']
        if 'grade' in obj:
            name += ' ('+str(obj['grade'])+')'
        else:
            name += ' ('+str(obj['credit'])+')'

        coordinate = self.semesterToCoordinate(semesterIndex)
        # y_offset = max(obj['numReverse_prerequisite'],obj['numPrerequisite'])* 20
        self.addList_num_subject(semesterIndex, obj['hasPrerequisite'], 0)

        x = coordinate['x']
        y = coordinate['y']

        cmp_semester = self.si.compare_semester(obj['year'], obj['semester'],
                                                self.last_year,
                                                self.last_semester)
        if cmp_semester < 0 or cmp_semester == 0:
            # if subjec_id.find('_old')  > 0:
            rect_fill = "#666666"
        else:
            if obj['hasPrerequisite']:
                rect_fill = "green"
            else: rect_fill = "#3498DB"

        return {
            "id": subjec_id,
            "type": "basic.Rect",
            "attrs": { "text": {
                         "text": name,
                         "fill": "white",
                         "font-family": "sans-serif" },
                      "rect": {
                         "fill": rect_fill,
                         "stroke": "white",
                         "rx": 5,
                         "ry": 5 } },
            "position":{"x": x,"y": y},
            "size":{"width": self.width,"height":self.height},
            "angle": 0,
            "z": 1
        }

    def createLink(self, obj):
        link_id = 'link' + obj['source'] + '-'+obj['target']
        source = obj['source']
        target = obj['target']
        return {
            "id": link_id,
            "type": "link",
            "source": { "id": source},
            "target": { "id": target},
            "z": 0,
            "router": { "name": "manhattan" },
            "connector": { "name": "rounded" },
            "attrs": {
                ".marker-source": { "d": "M 10 0 L 0 5 L 10 10 z" }
            }
        }

    def start(self, json_objects, num_year, num_semester):
        lists = list()
        lists += self.createSemesterLabelList(num_year, num_semester, json_objects['total_credits'])
        for json_object in json_objects['subjects']:
            lists.append(self.createSubject(json_object))
            # return lists
        for json_object in json_objects['links']:
            lists.append(self.createLink(json_object))
        return lists

    def get(self):
        return self.jointjs_object
