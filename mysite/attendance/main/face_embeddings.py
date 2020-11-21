#extracts faces from .npz compressed file and saves embeddings in compressed format
from numpy import load
from numpy import expand_dims
from numpy import asarray
from numpy import savez_compressed
from keras.models import  load_model
 
def get_embedding(model,face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean,std = face_pixels.mean(),face_pixels.std()
    face_pixels = (face_pixels-mean)/std
    samples = expand_dims(face_pixels, axis=0)
    yhat = model.predict(samples)
    return yhat[0]

def face_embeddings():
    data = load('attendance/model/sample_data.npz')
    trainX,trainy,testX,testy = data['arr_0'],data['arr_1'],data['arr_2'],data['arr_3']
    print('loaded:',trainX.shape,trainy.shape,testX.shape,testy.shape)

    model = load_model('attendance/model/facenet_keras.h5')
    newTrainX = list()

    for face_pixels in trainX:
        embedding = get_embedding(model,face_pixels)
        newTrainX.append(embedding)

    newTrainX = asarray(newTrainX)
    print(newTrainX.shape)

    newTestX = list()
    for face_pixels in testX:
        embedding = get_embedding(model,face_pixels)
        newTestX.append(embedding)
    newTestX = asarray(newTestX)
    print(newTestX.shape)
    savez_compressed('attendance/model/sample_data_face_embeddings.npz',newTrainX,trainy,newTestX,testy)

