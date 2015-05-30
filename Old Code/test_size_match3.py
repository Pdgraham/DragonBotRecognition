import numpy as np
import cv2

"""
Uses OpenCVs matchTemplate to find the emoticon in the image out of several possible emoicons
Initially runs matchTemplate on several scaled versions of an emoticon before preserving
	the size of the emoticon image that returned the best match
Then runs matchTemplate with each emoticon with the predicted image dimensions
Additionally: 
"""

#Test emoticon
emoticonPath = 'Emojis/1.png'
template = cv2.imread(emoticonPath)

#TEMP Taken image goes here
imagePath = 'testimg4.jpg'
image = cv2.imread(imagePath)
imageColor = cv2.imread(imagePath)

#Resize image taken and preserve image ratio
width = 800.0
r = float(width) / image.shape[1]
dim = (int(width), int(image.shape[0] * r))
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
imageColor = cv2.resize(imageColor, dim, interpolation = cv2.INTER_AREA)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
max_val = 0
imageThresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3)

#Find Best size in range using emoticon1 for now
for i in range(int(width)/10,int(width)/5,int(width)/100):
	width = i
	r = float(width) / template.shape[1]
	dim = (int(width), int(template.shape[0] * r))
	template = cv2.resize(template, dim, interpolation = cv2.INTER_AREA)
	templateGrey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	h,w = templateGrey.shape
	templateThres = cv2.adaptiveThreshold(templateGrey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 1)
	result = cv2.matchTemplate(imageThresh,templateThres, cv2.TM_CCOEFF)

	if cv2.minMaxLoc(result)[1] >= max_val:
		bestDim = (int(width), int(template.shape[0] * r))
		min_val0, max_val0, min_loc0, max_loc0 = cv2.minMaxLoc(result) # Located Region
		top_left = max_loc0
		bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(imageColor,top_left, bottom_right,(0,255,0),6)

space = 0
imageCropped = imageThresh[top_left[1] : bottom_right[1] ,
				top_left[0] : bottom_right[0]]

# imageCropped[0] = [0 for x in range(len(imageCropped[0]))]
# print imageThresh[0]
# cv2.imshow("Locally Searched Area",imageCropped)






max_val = 0
for i in range(1, 3):
	emoticonPath = 'Emojisirl/' + str(i) + 'irl.png'
	# emoticonPath = 'Emojis/' + str(i) + '.png'
	template = cv2.imread(emoticonPath)
	template = cv2.resize(template, bestDim, interpolation = cv2.INTER_AREA)
	templateGrey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	h,w = templateGrey.shape

	templateThres = cv2.adaptiveThreshold(templateGrey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 10)
	# result = cv2.matchTemplate(imageThresh,templateThres, cv2.TM_CCOEFF)
	result = cv2.matchTemplate(imageCropped,templateThres, cv2.TM_CCOEFF)

	if cv2.minMaxLoc(result)[1] >= max_val:
		templateThresh = templateThres
		foundEmoticon = template
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
		top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.imshow("Thresh of Found Emoticon", templateThresh)
cv2.imshow("Thresh of image", imageThresh)

# cv2.rectangle(imageColor,top_left, bottom_right,(0,0,255),6)
cv2.imshow("Found Emoticon", foundEmoticon)
cv2.imshow("Result", imageColor)
cv2.waitKey(0)