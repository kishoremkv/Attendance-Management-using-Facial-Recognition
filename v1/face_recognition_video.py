from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from scipy.spatial.distance import cosine
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input

def extract_faces ( filename, required_size = (224,224) ):
    pixels = pyplot.imread(filename)
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    faces_array = list()
    for result in results:
        x1,y1,width,height=result['box']
        x2,y2 = x1+width,y1+height
        face = pixels[y1:y2,x1:x2]
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        faces_array = faces_array.append(face_array)

    return faces_array

# pixels = extract_face('test1.jpg')
# pyplot.imshow(pixels)
# pyplot.show()

def get_embeddings(filenames):
    faces = list()
    # faces = [extract_face(f) for f in filenames]
    for f in filenames:
        x = extract_faces(f)
        faces = faces+x
    samples = asarray(faces,'float32')
    samples = preprocess_input(samples,version=2)
    model = VGGFace(model = 'resnet50',include_top=False,input_shape=(224,224,3),pooling='avg')
    yhat = model.predict(samples)
    return yhat

def is_match(known_embedding, candidate_embedding, thresh=0.5):
    score = cosine(known_embedding, candidate_embedding)
    if score<=thresh:
        print('>face is a Match (%.3f <=%.3f)' % (score,thresh))
    else:
        print('>face is Not a match (%.3f > %.3f)' % (score,thresh))

filenames = ['photo1.jpg','photo2.jpg','photo3.jpg','test1.jpg']
embeddings = get_embeddings(filenames)
kishore_id = embeddings[0]
is_match(kishore_id,embeddings[1])
is_match(kishore_id,embeddings[2])
is_match(kishore_id,embeddings[3])

