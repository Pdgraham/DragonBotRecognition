import numpy as np
import cv2
import cv
import scipy.spatial

img = cv2.imread('testimg5.jpg')
#Resize image taken and preserve image ratio
width = 800.0
minArea = 1000
maxArea = 100000
r = float(width) / img.shape[1]
dim = (int(width), int(img.shape[0] * r))
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imggray,127,255,0)
# image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# removes the empty contours, too small to be shapes
emptyContours = []
emptyIndex = []
for index in range(len(contours)):
	if cv2.contourArea(contours[index]) <= minArea or cv2.contourArea(contours[index]) >= maxArea:
		emptyContours.append(index)
shift = 0
for conts in emptyContours:
	contours = np.delete(contours, conts - shift)
	shift += 1

# approximate shape, assign general shape

squares = []
triangles = []
arrows = []
for cnt in range(len(contours)):
	contours[cnt] = cv2.approxPolyDP(contours[cnt],0.05*cv2.arcLength(contours[cnt],True),True)

# delete overlapping (useless contours) hash the approximate location?
blocks = []
for index in range(len(contours)):
	if len(blocks) != 0:
		fit = False
		for block in range(len(blocks)):
			if np.abs(np.linalg.norm(np.average(blocks[block][0],0) - np.average(contours[index],0))) < 50.0: # make this a function of how large the page is
				blocks[block].append(contours[index])
				fit = True
		if not fit:
			blocks.append([contours[index]])
	else:
		blocks.append([contours[index]])

delete = []
deleteBlocks = []
shift = 0
for index in range(len(blocks)):
	if len(blocks[index]) > 2:
		largest = None
		secondLargest = None
		for index2 in range(len(blocks[index])):

			if largest == None or cv2.contourArea(np.asarray(blocks[index][index2])) > cv2.contourArea(np.asarray(largest)):
				if secondLargest != None:
					delete.append(secondLargest)
				if largest != None:
					secondLargest = largest
				largest = blocks[index][index2]
			elif (secondLargest == None or cv2.contourArea(np.asarray(blocks[index][index2])) > cv2.contourArea(np.asarray(secondLargest))):
				
				if secondLargest != None:
					delete.append(secondLargest)
				secondLargest = blocks[index][index2]
			else:
				delete.append(blocks[index][index2])
				deleteBlocks.append(blocks[index][index2])
		# indexs = []
		# for conts in deleteBlocks:
		# 	if conts in blocks[index]:
		# 		indexs.append(index)
		# blocks = np.delete(contours, indexs)
		# for x in range(len(blocks)):
		# 	print len(blocks[x])
			

indexs = []
for conts in delete:
	for index in range(len(contours)):
		if conts in contours[index]:
			indexs.append(index)
contours = np.delete(contours, indexs)

blocks = []
for index in range(len(contours)):
	if len(blocks) != 0:
		fit = False
		for block in range(len(blocks)):
			if np.abs(np.linalg.norm(np.average(blocks[block][0],0) - np.average(contours[index],0))) < 50.0: # make this a function of how large the page is
				blocks[block].append(contours[index])
				fit = True
		if not fit:
			blocks.append([contours[index]])
	else:
		blocks.append([contours[index]])

# print pairs
pairs = []
for cnt in range(len(contours)):
	if len(contours[cnt]) == 3:
		triangles.append(contours[cnt])
	elif len(contours[cnt]) == 4:
		squares.append(contours[cnt])
	else:
		print cnt
		pairs.append(contours[cnt])
		rows,cols = imggray.shape[:2]
		[vx,vy,x,y] = cv2.fitLine(contours[cnt], cv2.cv.CV_DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y)
		righty = int(((cols-x)*vy/vx)+y)
		leftx=cols-1
		rightx=0
		cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
		arrows.append(contours[cnt])
		# print lefty, righty, width

		# pairs += [(lefty-righty) /  float(width)]

# print pairs

# print blocks[0]
# print blocks[0][0]
# # print np.linalg.eig(blocks[0][0])
# print np.mean(blocks[0][0],0) 
# quit()

blockPairs = []
for x in range(len(pairs)):
	closestNodes = []
	closestDistance = 10000
	for i in range(len(blocks)):
		for j in range(len(blocks)):

			# print pairs[x]
			# print "HIII"
			if blocks[i] is not blocks[j] and len(blocks[i]) == 2 and len(blocks[j]) ==2:
				tempSet = list(blocks[i][0]) + list(blocks[j][0])
				# print np.mean(pairs[x],0), np.subtract(np.mean(tempSet,0))
				# tempSet 
				distance = np.linalg.norm(np.subtract(np.mean(pairs[x],0),np.subtract(np.mean(tempSet),0)))
				# print distance, closestDistance
				if distance < closestDistance:
					closestNodes = [blocks[j][0],blocks[i][0]]
					closestDistance = distance
					k = [i,j]

	if len(closestNodes) == 2:
		blockPairs.append(closestNodes[0])
		blockPairs.append(closestNodes[1])
	
		print k



# cv2.drawContours(img, [blocks[1][0]], -1, (255,0,0), 3)

# cv2.drawContours(img, blockPairs, -1, (255,0,0), 3)
# cv2.drawContours(img, triangles, -1, (255,0,0), 3)
cv2.drawContours(img, squares, -1, (0,255,0), 3)
# cv2.drawContours(img, arrows, -1, (0,0,255), 3)

cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('img',img)
while True:
	if cv2.waitKey(0)  == 27:
		break

cv2.destroyAllWindows()