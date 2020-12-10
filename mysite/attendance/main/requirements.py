import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.preprocessing import Normalizer
import pickle
from attendance.models import *

def normalize(img):
    mean, std = img.mean(),img.std()
    return (img-mean)/std

def get_encoding(face_encoder, face, size):
    face = normalize(face)
    face = cv2.resize(face,size) #for resizing to (160,160,3)
    encoding = face_encoder.predict(np.expand_dims(face,axis=0))[0] #for making 2D
    return encoding

def get_face(img,box):
    x1,y1,w,h = box
    x1, y1 = abs(x1),abs(y1)
    x2, y2 = x1+w,y1+h
    face = img[y1:y2,x1:x2]
    return face,(x1,y1),(x2,y2)

l2_normalizer = Normalizer('l2')

def plt_show(cv_img):
    img_rgb = cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.show()

def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict

def save_pickle(path,obj):
    with open(path,'wb') as f:
        pickle.dump(obj,f)

def post_student_info(user):
    print(user)
    try:
        cur_class = Class.objects.get(section = user['section'], branch = user['branch'])
        print(user['naCme'])  
        new_student = Student(roll_no = user.get('roll_no'), name = user.get('name'), section = cur_class)
        new_student.save()
        print("Added student info!"+" "+user['name'])
    except Class.DoesNotExist:
        return False
    return True




