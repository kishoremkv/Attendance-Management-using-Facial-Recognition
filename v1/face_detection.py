
# face detection with mtcnn on a photograph

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN

# draw an image with detected objects
def draw_image_with_boxes(filename, result_list):
	data = pyplot.imread(filename)
	# plot the image
	pyplot.imshow(data)
	# get the context for drawing boxes
	ax = pyplot.gca()
	# plot each box
	for result in result_list:
		# get coordinates
		x, y, width, height = result['box']
		# create the shape
		rect = Rectangle((x, y), width, height, fill=False, color='red')
		# draw the box
		ax.add_patch(rect)
	# show the plot
	pyplot.show()

def draw_faces(filename,result_list):
	data = pyplot.imread(filename)

	for i in range(len(result_list)):
		x1,y1,width,height = result_list[i]['box']
		x2,y2 = x1+width,y1+height

		pyplot.subplot(1,len(result_list),i+1)
		pyplot.axis('off')
		pyplot.imshow(data[y1:y2,x1:x2])
	pyplot.show()



filename = 'test2.jpg'
# load image from file
pixels = pyplot.imread(filename)
print(pixels.shape)
# create the detector, using default weights
detector = MTCNN()
# detect faces in the image
faces = detector.detect_faces(pixels)
# display faces on the original image
draw_image_with_boxes(filename, faces)
draw_faces(filename,faces)
