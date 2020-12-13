from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse
from .models import *
import os,threading
import cv2
from .main.face_embeddings import *
from .main.face_recognition_video import *
from .main.save_faces import *
from .main.face_classification import *
from .main.requirements import *
from .forms import FileUpload
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from .main.response_codes import get_response_status
import json
from .main.utils import *
from django.views.decorators.gzip import gzip_page

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
            if post_student_info(request.POST):
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
                print("Student not added!")
        else:
            print("Files not uploaded!")
        return redirect('/attendance')  

    else:
         form = FileUpload()
    return render(request, 'attendance/add_student.html')

def start_streaming(request):
    face_recognition_video()
    return render(request, 'attendance/start_streaming.html')



@csrf_exempt
def display(request):
    if request.method == "POST":
        print(request.POST)  

        if "section_info" in request.POST.keys():
            # print(request.POST)
            print("came to section info")
            branch = request.POST["section_info"]
            status_code = 200
            sections_info = get_all_sections(branch)  
            return HttpResponse(json.dumps({'Message': 'Success!', 'data': sections_info}, cls=Encoder),
                            content_type="application/json", status=get_response_status(status_code))

        elif "section_no" in request.POST.keys() and "class_name" in request.POST.keys():
            print("came to section no and class no")
            try:
                section_attendance,status_code = get_section_attendance(request.POST['class_name'],request.POST['section_no'],request.POST['period_no'],request.POST['date'])
                if status_code==200:
                    return HttpResponse(json.dumps({'Message': 'Success!', 'data': section_attendance}, cls=Encoder),
                                content_type="application/json", status=get_response_status(status_code))
                else:
                    return HttpResponse(json.dumps({'Message': 'failure'}, cls=Encoder),
                                content_type="application/json", status=get_response_status(status_code))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({'Message': 'failure'}, cls=Encoder),
                                content_type="application/json", status=get_response_status(500))
        else:
            print("came to else part")
            all_branches = get_all_branches()
            status_code = 200
            return HttpResponse(json.dumps({'Message': 'Success!', 'data': all_branches}, cls=Encoder),
                            content_type="application/json", status=get_response_status(status_code))
            
    return render(request, 'attendance/display.html')






# # def video_streaming(request):
# #     return StreamingHttpResponse(face_recognition_video())
# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         image = self.frame
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

#     def update(self):
#         while True:
#             (self.grabbed, self.frame) = self.video.read()


# vc= VideoCamera()


# def gen(camera):
#     while vc.isOpened() :
#         ret,frame = vc.read()
#         if not ret:
#             break
#         cv2.imshow('camera',frame)
#         yield(b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         if cv2.waitKey(1) & 0xFF==ord('q'):
#             temp = False


# @gzip_page
# def video_streaming(request):
#     try:
#         return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:  # This is bad! replace it with proper handling
#         pass