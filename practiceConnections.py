import numpy as np
import cv2

minArea = 1000
maxArea = 100000

img = cv2.imread('sheet5.jpg')
#Resize image taken and preserve image ratio
width = 800.0
r = float(width) / img.shape[1]
dim = (int(width), int(img.shape[0] * r))
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

img2 = cv2.imread('sheet4.jpg')
#Resize image taken and preserve image ratio
width = 800.0
r = float(width) / img.shape[1]
dim = (int(width), int(img.shape[0] * r))
img2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)


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
	if len(contours[cnt]) == 3:
		triangles.append(contours[cnt])
	elif len(contours[cnt]) == 4:
		squares.append(contours[cnt])
	else:
		rows,cols = imggray.shape[:2]
		[vx,vy,x,y] = cv2.fitLine(contours[cnt], cv2.cv.CV_DIST_L2,0,0.01,0.01)
		lefty = int((-x*vy/vx) + y)
		righty = int(((cols-x)*vy/vx)+y)
		cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
		# cv2.line(img2,(cols-1,righty),(0,lefty),(0,255,0),2)

		arrows.append(contours[cnt])


cv2.drawContours(img, triangles, -1, (255,0,0), 3)
cv2.drawContours(img, squares, -1, (0,255,0), 3)
cv2.drawContours(img, arrows, -1, (0,0,255), 3)

# cv2.drawContours(img, contours, -1, (0,255,0), 3)

cv2.imshow('img',img)
while True:
	if cv2.waitKey(0)  == 27:
		break

cv2.destroyAllWindows()