#saves the final model in pkl file
from numpy import savez_compressed,load
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from .requirements import *


def face_classification():
    data = load('attendance/model/sample_data_face_embeddings.npz')
    trainX,trainy, testX,testy = data['arr_0'],data['arr_1'],data['arr_2'],data['arr_3']
    print("Dataset: train %d,test=%d" %(trainX.shape[0],testX.shape[0]))

    in_encoder = Normalizer(norm='l2')
    in_encoder.fit(trainX)
    trainX = in_encoder.transform(trainX)
    testX = in_encoder.transform(testX)

    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    save_pickle('attendance/model/label_encoder.pkl',out_encoder)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)
 
    model = SVC(kernel="linear", probability=True)
    model.fit(trainX,trainy)

    yhat_train = model.predict(trainX)
    yhat_test = model.predict(testX)

    #saving the model in pkl file
    save_pickle('attendance/model/svm_model.pkl',model)

    score_train = accuracy_score(trainy,yhat_train)
    score_test = accuracy_score(testy,yhat_test)
    print('Accuracy: train=%.3f, test=%.3f' %(score_train*100,score_test*100))
    print("Training is done!!!")
