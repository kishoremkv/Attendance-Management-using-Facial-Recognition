from keras.models import load_model
from PIL import Image
from numpy import asarray
model = load_model("model/facenet_keras.h5")
print(model.inputs)
print(model.outputs)
filename = 'db/students/Kishore/photo1.jpg'

image = Image.open(filename)
# assert isinstance(image, object)
print(image)
print(asarray(image))
