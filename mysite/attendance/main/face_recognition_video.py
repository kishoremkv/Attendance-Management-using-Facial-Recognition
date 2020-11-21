from .requirements import *
from keras.models import  load_model
from mtcnn import MTCNN
from datetime import datetime
import numpy as np
import cv2


def get_embedding(facenet_model,face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean,std = face_pixels.mean(),face_pixels.std()
    face_pixels = (face_pixels-mean)/std
    samples = np.expand_dims(face_pixels, axis=0)
    yhat = facenet_model.predict(samples)
    return yhat[0]

def recognize(img, facenet_model, svm_model, detector, labels, confidence = 0.99, required_size=(160,160)):
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence']<confidence:
            continue
        face,p1,p2 = get_face(img_rgb,res['box'])
        face = cv2.resize(face,required_size)
        encode = get_embedding(facenet_model,face)
        # print(type(encode),encode)
        trainX = np.reshape(encode, (-1, len(encode)))
        in_encoder = Normalizer(norm='l2')
        in_encoder.fit(trainX)
        trainX = in_encoder.transform(trainX)
        name = -1
        
        # print(type(trainX),trainX)
        name = svm_model.predict(trainX)
        # print(type(name),name)
        # print(labels.inverse_transform(name))
        detected_person = labels.inverse_transform(name)[0]
        name = name[0]        
        if name ==-1:
            cv2.rectangle(img,p1,p2,(0,0,255),2)
            cv2.putText(img,name,p1,cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),3)
        else:
            cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
            cv2.putText(img, detected_person, (p1[0], p1[1] - 5), cv2.FONT_HERSHEY_PLAIN, 1,(0, 200, 200), 3)
            print(detected_person+" "+str(datetime.now()))
    return img

def face_recognition_video():
    face_detector = MTCNN()
    facenet_model = load_model("attendance/model/facenet_keras.h5")
    svm_model = load_pickle("attendance/model/svm_model.pkl")
    labels = load_pickle("attendance/model/label_encoder.pkl")
    vc = cv2.VideoCapture(0)

    while vc.isOpened():
        ret,frame = vc.read()
        if not ret:
            break
        frame = recognize(frame,facenet_model, svm_model, face_detector, labels)
        cv2.imshow('camera',frame)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
