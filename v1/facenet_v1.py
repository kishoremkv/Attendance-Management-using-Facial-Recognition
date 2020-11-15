from keras_facenet import FaceNet
import numpy as np
from keras.models import load_model
import cv2
from scipy.spatial.distance import cosine
model = load_model('model/facenet_keras.h5')
# print(model.inputs)
# print(model.outputs)

def is_match(known_embedding, candidate_embedding, thresh=0.5):
    score = cosine(known_embedding, candidate_embedding)
    if score<=thresh:
        print('>face is a Match (%.3f <=%.3f)' % (score,thresh))
    else:
        print('>face is Not a match (%.3f > %.3f)' % (score,thresh))


embedder = FaceNet()
image = cv2.imread('images/test2.jpg')
# x = embedder.extract('images/test2.jpg',0.95)#for detecting the faces and getting the embeddings as a dictionary
embeddings= embedder.embeddings([image])# for getting embeddings of particular image
print(len(embeddings[0]))

filenames = ['images/photo1.jpg','images/photo2.jpg','images/photo3.jpg','images/test1.jpg']
images = list()
for file in filenames:
    image = cv2.imread(file)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    images.append(image)

embeddings = embedder.embeddings(images)
mean, std = embeddings.mean(), embeddings.std()
embeddings = (embeddings - mean) / std


kishore_id = embeddings[0]
print(len(kishore_id))
is_match(kishore_id,embeddings[1])
is_match(kishore_id,embeddings[2])
is_match(kishore_id,embeddings[3])
