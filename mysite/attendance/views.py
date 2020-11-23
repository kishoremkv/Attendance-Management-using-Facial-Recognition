from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .main.face_embeddings import *
from .main.face_recognition_video import *
from .main.save_faces import *
from .main.face_classification import *
# Create your views here.
# django searches for templates folder in the particular app to process the html files

def index(request):
    students_info = Student.objects.all()

    if request.method == "POST":
        files = request.FILES.getlist("files")
        print("hello", files)
        for file in files:
            print(file)
    return render(request, 'attendance/index.html', { 'students_info' : students_info })

def train_model(request):
    # call the html file
    save_faces()
    face_embeddings()
    face_classification()
    return render(request, 'attendance/train.html')

def add_student(request):
    return render(request, 'attendance/add_student.html')

def start_streaming(request):
    face_recognition_video()
    return render(request, 'attendance/start_streaming.html')