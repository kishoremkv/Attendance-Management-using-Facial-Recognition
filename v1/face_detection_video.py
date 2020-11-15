# face detection with mtcnn on a photograph

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN
import cv2


# draw an image with detected objects
def draw_image_with_boxes(pixels, result_list):
    # data = pyplot.imread(filename)
    data = pixels
    # pyplot.imshow(data)
    ax = pyplot.gca()
    for result in result_list:
        # get coordinates
        x, y, width, height = result['box']
        print(result['box'])
        cv2.rectangle(data, (x, y), (x+width, y+height), (255, 0, 0), 2)
        # rect = Rectangle((x, y), width, height, fill=False, color='red')
        # ax.add_patch(rect)
    cv2.imshow('img2',data)
    # show the plot
    # pyplot.show()


def draw_faces(pixels, result_list):
    data = pixels
    for i in range(len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        pyplot.imshow(data[y1:y2, x1:x2])
    pyplot.show()


cap = cv2.VideoCapture(0)
detector = MTCNN()
while True:
    # Read the frame
    _, pixels = cap.read()
    # cv2.imshow('img', pixels)
    faces = detector.detect_faces(pixels)
    draw_image_with_boxes(pixels, faces)
    # draw_faces(pixels, faces)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# filename = 'test2.jpg'
# # load image from file
# pixels = pyplot.imread(filename)
# # create the detector, using default weights

# detect faces in the image
