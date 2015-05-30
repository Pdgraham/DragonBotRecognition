import cv2
import numpy as np

minAreaContours = 1000
maxAreaContours = 100000

def findContours(img):

	# Resize image taken and preserve image ratio
	width = 800.0
	r = float(width) / img.shape[1]
	dim = (int(width), int(img.shape[0] * r))
	img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

	imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imggray,127,255,0)
	imageThresh = cv2.adaptiveThreshold(imggray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	return contours

"""
inputs:

outputs:
emoticons - emojis found on the page enclosed by squares or triangles
arrows - ~7 points representing a black arrow between two shapes
"""
def extractShapes(originalContours, img, drawContours = False):
	contours = removeSmallContours(originalContours)
	contours, emoticons = approximateShapes(contours)
	triangles, squares, arrows = findShapes(contours)
	if drawContours:
		cv2.drawContours(img, contours, -1, (255,0,0), 3)
		cv2.drawContours(img, arrows, -1, (0,0,255), 3)
		cv2.drawContours(img, emoticons, -1, (0,255,0), 3)
		# cv2.drawContours(img,originalContours, -1, (255,0,0), 3)
	
	return emoticons, arrows, contours

# removes the empty contours, too small to be shapes
def removeSmallContours(contours, minArea = minAreaContours, maxArea = maxAreaContours):
	emptyContours = []
	emptyIndex = []
	for index in range(len(contours)):
		if cv2.contourArea(contours[index]) <= minArea or cv2.contourArea(contours[index]) >= maxArea:
			emptyContours.append(index)
	shift = 0
	for conts in emptyContours:
		contours = np.delete(contours, conts - shift)
		shift += 1
	return contours

"""
approximate shape, and removes extra shapes
reduces contours to pairs of emoticons and squares or triangles, and arrows
"""
def approximateShapes(contours, approximationAccuracy = 0.05):
	closed = True
	for cnt in range(len(contours)):
		# Approximates a polygonal curve(s) with the specified precision.
		contours[cnt] = cv2.approxPolyDP(contours[cnt],approximationAccuracy*cv2.arcLength(contours[cnt],closed),closed)

	"""
	delete overlapping (useless) contours
	seperates the contours into sets of contours (blocks) by their proximaty to each other
	removes contours that are not the two largest our of the blocks
	mostly necessary for emoticons that are identified as several stacked contours
	"""
	blocks = []
	for index in range(len(contours)):
		if len(blocks) != 0:
			fit = False
			for block in range(len(blocks)):
				# TODO make this a function of how large the page is
				if np.abs(np.linalg.norm(np.average(blocks[block][0],0) - np.average(contours[index],0))) < 50.0:
					blocks[block].append(contours[index])
					fit = True
			if not fit:
				blocks.append([contours[index]])
		else:
			blocks.append([contours[index]])

	delete = []
	deleteBlocks = []
	emoticons = []
	shift = 0
	for index in range(len(blocks)):
		if len(blocks[index]) >= 2:
			largest = []
			secondLargest = []
			for index2 in range(len(blocks[index])):
				if len(largest) == 0 or cv2.contourArea(np.asarray(blocks[index][index2])) > cv2.contourArea(np.asarray(largest)):
					if len(secondLargest) == 0:
						delete.append(secondLargest)
					if len(largest) != 0:
						secondLargest = largest
					largest = blocks[index][index2]
				elif (len(secondLargest) == 0 or cv2.contourArea(np.asarray(blocks[index][index2])) > cv2.contourArea(np.asarray(secondLargest))):
					if len(secondLargest) != 0:
						delete.append(secondLargest)
					secondLargest = blocks[index][index2]
				else:
					delete.append(blocks[index][index2])
					deleteBlocks.append(blocks[index][index2])

			emoticons.append(secondLargest)

	indexs = []
	for conts in delete:
		for index in range(len(contours)):
			if conts in contours[index]:
				indexs.append(index)
	contours = np.delete(contours, indexs)

	return contours, emoticons

""" Assigns contours to either a triangle, square, or arrow based on number of sides/vertices """
def findShapes(contours):
	squares = []
	triangles = []
	arrows = []
	for cnt in range(len(contours)):
		if len(contours[cnt]) == 3:
			triangles.append(contours[cnt])
		elif len(contours[cnt]) == 4:
			squares.append(contours[cnt])
		else:
			arrows.append(contours[cnt])
	return triangles, squares, arrows