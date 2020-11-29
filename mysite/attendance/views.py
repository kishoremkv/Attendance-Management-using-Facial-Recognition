from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
import os
from .main.face_embeddings import *
from .main.face_recognition_video import *
from .main.save_faces import *
from .main.face_classification import *
from .forms import FileUpload
from .models import UploadFile
from django.core.files.storage import FileSystemStorage
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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
    if request.method == "POST":
        form = FileUpload(request.POST, request.FILES)
        print(request.POST)
        files = request.FILES.getlist('files')
        if form.is_valid() and len(files)==20:
            for i in range(0,len(files)):
                f = files[i]
                # file_instance = UploadFile(files=f)
                # file_instance.save()
                # for storing files in the specific directory with rollno as a directory name
                location = os.path.join(BASE_DIR,'attendance/images/train/'+request.POST['roll_no']+'/')
                if i in range(15,20):
                    location = os.path.join(BASE_DIR,'attendance/images/val/'+request.POST['roll_no']+'/')
                print(str(location)) 
                fs = FileSystemStorage(location = location ) 
                file = fs.save(f.name, f) 
                fileurl = fs.url(file) 

            print("Uploaded files successfully!")
        else:
            print("files not uploaded!")
        return redirect('/attendance')  

    else:
         form = FileUpload()
    return render(request, 'attendance/add_student.html')

def start_streaming(request):
    face_recognition_video()
    return render(request, 'attendance/start_streaming.html')
