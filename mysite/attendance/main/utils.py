import json
from bson.objectid import ObjectId
import datetime
from attendance.models import *
from django.core import serializers

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj

def get_all_branches():
    branches = list()
    all_branches = Class.objects.values('branch').distinct()
    for x in all_branches:
        branches.append(x['branch'])
    print(branches)
    return branches

def get_all_sections(branch):
    all_sections = Class.objects.filter(branch = branch)
    sections = list()
    for x in all_sections:
        print(x.section)
        sections.append(x.section)
    return sections

def get_section_attendance(branch, section_no,period,date):
    attendance = list()
    try:
        date = date.split('-')
        date = str(date[2])+"/"+str(date[1])+"/"+str(date[0])
        print(branch,section_no,period,date)

        student_attendance = Attendance.objects.filter(branch = branch,section = section_no, period = period,date = date )
        for x in student_attendance:
            cur_attendance = dict()
            cur_attendance['roll_no'] = x.roll_no
            cur_attendance['period'] = x.period
            cur_attendance['section'] = x.section
            cur_attendance['branch'] = x.branch
            cur_attendance['section'] = x.section
            cur_attendance['date'] = x.date
            cur_attendance['time'] = x.time
            cur_attendance['status'] = x.status
            # cur_attendance = serializers.serialize("json",x)
            print(cur_attendance)
            attendance.append(cur_attendance)
        return attendance,200
    except Exception as e:
        print(e)
        return attendance,500