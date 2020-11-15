# which produces encodings.pkl file
import os

import mtcnn
from keras.models import load_model

from requirements import *

facenet_model = 'model/facenet_keras.h5'
students_dir = 'db/students'
encodings_path = 'data/encodings/encodings.pkl'
required_size = (160,160)

face_detector = mtcnn.MTCNN()
encoding_model = load_model(facenet_model)

encoding_dict = dict()

for student_name in os.listdir(students_dir):
    student_dir = os.path.join(students_dir,student_name)
    encodes=[]

    for img_name in os.listdir(student_dir):
        img_path = os.path.join(student_dir,img_name)
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = face_detector.detect_faces(img_rgb)

        if results:
            res = max(results, key = lambda b: b['box'][2]*b['box'][3])
            face,_,_ = get_face(img_rgb,res['box'])

            face = normalize(face)
            face = cv2.resize(face,required_size)
            encode = encoding_model.predict(np.expand_dims(face,axis=0))[0]
            encodes.append(encode)
    if encodes:
        encode = np.sum(encodes, axis=0)
        encode = l2_normalizer.transform(np.expand_dims(encode,axis=0))[0]
        encoding_dict[student_name]=encode

for key in encoding_dict.keys():
    print(key)

save_pickle(encodings_path,encoding_dict)


