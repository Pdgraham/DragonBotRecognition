import cv2

from contours import extractShapes, findContours
from emojis import identifyEmoticons, findPath

if __name__ == '__main__':

	img = cv2.imread('testimg5.jpg')
	
	allContours = findContours(img)
	emoticons, arrows, narrowedContours = extractShapes(allContours, img, drawContours = True)
	identifyEmoticons(img, emoticons, showEmojis = True)
	findPath(emoticons, arrows, img)

	""" shows image that is exited on any key press """
	cv2.imshow('Image',img)
	while True:
		if cv2.waitKey(0)  == 27:
			break
	cv2.destroyAllWindows()