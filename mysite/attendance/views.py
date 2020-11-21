from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
# Create your views here.
# django searches for templates folder in the particular app to process the html files

def index(request):
    students_info = Student.objects.all()
    return render(request, 'attendance/index.html', { 'students_info' : students_info })

def train_model(request):
    # 
    # call the html file
    return render(request, 'attendance/train.html')

def add_student(request):

    return render(request, 'attendance/add_student.html')
