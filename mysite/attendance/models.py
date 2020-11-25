from django.db import models

# Create your models here.

#faculty has a name and id
class Faculty(models.Model):
    faculty_id = models.CharField(max_length = 10, default = "")
    name = models.CharField(max_length = 32, default = "")

    def __unicode__(self):
        return self.name

# each subject has a faculty (one to many)
# each subject has id, name and faculty info
class Subject(models.Model):
    subject_id = models.CharField(max_length = 10, default = "")
    subject_name = models.CharField(max_length = 32, default = "")
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.subject_name

# each class on a particular day has 7 periods
# each period has a subject and vice versa
class DailyTimeTable(models.Model):
    period1 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period1")
    period2 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period2")
    period3 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period3")
    period4 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period4")
    period5 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period5")
    period6 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period6")
    period7 = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name = "period7")

# each class has a weekly time table
# each day has a daily time table which is one to one
class WeeklyTimeTable(models.Model):
    tuesday = models.OneToOneField(DailyTimeTable,   on_delete=models.CASCADE, related_name = "tuesday")
    wednesday = models.OneToOneField(DailyTimeTable, on_delete=models.CASCADE, related_name = "wednesday")
    thursday = models.OneToOneField(DailyTimeTable,  on_delete=models.CASCADE, related_name = "thursday")
    friday = models.OneToOneField(DailyTimeTable,    on_delete=models.CASCADE, related_name = "friday")
    saturday = models.OneToOneField(DailyTimeTable,  on_delete=models.CASCADE, related_name = "saturday")

# there are many classes 
# each class has branch, year, # of students and time table
# every class is assigned with a weekly time table
class Class(models.Model):
    branch = models.CharField(max_length = 5, default = "")
    section = models.CharField(max_length = 2, default = "")
    year = models.IntegerField(default = 1)
    no_of_students = models.IntegerField(default = 60)
    time_table = models.OneToOneField(WeeklyTimeTable, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.branch+" "+self.year+self.section

# for every subject attendance has to be taken 
class SubjectAttendanceTable(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    attendance_count = models.IntegerField(default = 0)

# each student has 6 subjects
# each subject has attendance to be maintained
class StudentAttendanceTable(models.Model):
    subject1 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject1")
    subject2 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject2")
    subject3 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject3")
    subject4 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject4")
    subject5 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject5")
    subject6 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject6")
    subject7 = models.OneToOneField(SubjectAttendanceTable, on_delete=models.CASCADE, related_name = "subject7")


# every student has a class (many to one)
# every student has roll_no, name, section and attendance
# attendance is the collection of all his subjects
class Student(models.Model):
    roll_no = models.CharField(max_length = 10, default = "")
    name = models.CharField(max_length = 32, default = "")
    section = models.ForeignKey(Class, on_delete=models.CASCADE)
    # attendance = models.OneToOneField(StudentAttendanceTable, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.roll_no


class Attendance(models.Model):
    roll_no = models.CharField(max_length = 10, default = "")
    # we will get name, class and section from the rollno
    section = models.CharField(max_length = 10, default = "")
    period = models.CharField(max_length = 10, default = "")
    date = models.CharField(max_length = 10, default = "")
    status = models.CharField(max_length = 10, default = "Absent")

    def __unicode__(self):
        return self.roll_no + self.section + self.period 