#recognizing the images using encodings.pkl file
from scipy.spatial.distance import cosine
import numpy as np
import cv2
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
from requirements import plt_show,get_face,get_encoding,load_pickle,l2_normalizer

facenet_model = '../model/facenet_keras.h5'
students_dir = '../db/students'
encodings_path = '../data/encodings/encodings.pkl'
test_img_path = '../data/test/test2.jpg'
test_res_path = '../data/results/res.jpg'

required_size = (160,160)
cosine_limit = 0.3

face_detector = MTCNN()
encoding_model = load_model(facenet_model)
encodings_dict = load_pickle(encodings_path)

img = cv2.imread(test_img_path)
plt_show(img)

img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
results = face_detector.detect_faces(img_rgb)

for res in results:
    face,p1,p2 = get_face(img_rgb,res['box'])
    encode = get_encoding(encoding_model,face,required_size)
    encode = l2_normalizer.transform(np.expand_dims(encode,axis=0))[0]

    name = 'Not Present'
    distance = float("inf")

    for db_name, db_encode in encodings_dict.items():
        dist = cosine(db_encode,encode)
        if dist < cosine_limit and dist < distance:
            name = db_name
            distance = dist

    if name == 'Not Present':
        cv2.rectangle(img, p1,p2,(0,0,255),3)
        cv2.putText(img,name,p1,cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),3)
    else:
        cv2.rectangle(img, p1, p2, (0, 255, 0), 3)
        cv2.putText(img, name + f'{distance:.2f}', p1, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)


cv2.imwrite(test_res_path,img)
plt_show(img)




