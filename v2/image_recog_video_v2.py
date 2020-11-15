from scipy.spatial.distance import cosine
from requirements import *
from mtcnn import MTCNN
from datetime import datetime
from keras.models import load_model



def recognize(img, detector, encoder, encoding_dict,cosine_limit=0.5,
              confidence = 0.99,
              required_size=(160,160)):
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence']<confidence:
            continue
        face,p1,p2 = get_face(img_rgb,res['box'])
        encode = get_encoding(encoder,face,required_size)
        encode = l2_normalizer.transform(encode.reshape(1,-1))[0]
        name = 'Not Present'

        distance = float("inf")
        for db_name,db_encode in encoding_dict.items():
            dist = cosine(db_encode,encode)

            if dist<cosine_limit and dist<distance:
                name = db_name
                distance=dist

        if name =='Not Present':
            cv2.rectangle(img,p1,p2,(0,0,255),2)
            cv2.putText(img,name,p1,cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),3)
        else:
            cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
            cv2.putText(img, name + f' {distance:.2f}', (p1[0], p1[1] - 5), cv2.FONT_HERSHEY_PLAIN, 1,(0, 200, 200), 3)
            print(name+" "+str(datetime.now()))
    return img

facenet_model = '../model/facenet_keras.h5'
encodings_path = '../data/encodings/encodings.pkl'

face_detector = MTCNN()
encoding_model = load_model(facenet_model)
encodings_dict = load_pickle(encodings_path)

vc = cv2.VideoCapture(0)

while vc.isOpened():
    ret,frame = vc.read()
    if not ret:
        break
    frame = recognize(frame,face_detector,encoding_model,encodings_dict)
    cv2.imshow('camera',frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
