import cv2
import numpy as np

def identifyEmoticons(image, emoticons, showEmojis = False):
	imageGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	imageThresh = cv2.adaptiveThreshold(imageGrey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5) # 9,3
	correctEmoticons = []
	correctEmoticons2 = []
	for j in range(len(emoticons)):
		xmax, ymax = emoticons[j].max(axis=0)[0]
		xmin, ymin = emoticons[j].min(axis=0)[0]
		width = np.subtract(xmax, xmin)
		height = np.subtract(ymax, ymin)
		matchValue = 0

		for i in range(1, 15):
			emoticonPath = 'Emojis/' + str(i) + '.png'
			template = cv2.imread(emoticonPath)
			proportion = 0.90
			bestDim = (int(width*proportion), int(height*proportion))
			# bestDim = (int(width), int(height))
			template = cv2.resize(template, bestDim, interpolation = cv2.INTER_AREA)

			templateGrey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
			h,w = templateGrey.shape

			templateThres = cv2.adaptiveThreshold(templateGrey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 9)

			top_left = (xmin,ymin)
			bottom_right = (top_left[0] + width, top_left[1] + height)
			imageCropped = imageThresh[top_left[1] : bottom_right[1] ,
						top_left[0] : bottom_right[0]]
			result = cv2.matchTemplate(imageCropped,templateThres, cv2.TM_CCOEFF_NORMED)
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
			if matchValue <= max_val:
				matchValue = max_val
				correctEmoticon = emoticonPath
				templateThres2 = templateThres
		correctEmoticons2 += [templateThres2]
		correctEmoticons.append(correctEmoticon)

	print "Filepath of Identified Emoticons:" , correctEmoticons

	""" Displays the emoticons that were found """
	if showEmojis:
		for k in range(len(correctEmoticons)):
			matchEmoticon = cv2.imread(correctEmoticons[k])
			# cv2.imshow("hey there", imageThresh)
			cv2.imshow("Emoji: " + str(k), matchEmoticon)

			


def findPath(emoticons, arrows, img):
	connections = []
	for x in range(len(arrows)):
		closestNodes = []
		closestDistance = 10000000
		rect = cv2.boundingRect(arrows[x])
		cv2.circle(img, (int(rect[0]+(rect[2]/2.0)),int(rect[1]+(rect[3]/2))), 5, (0,0,255))
		cv2.circle(img, (int(np.mean(arrows[x],0)[0][0]),int(np.mean(arrows[x],0)[0][1])), 5, (0,255,0))
		for i in range(len(emoticons)):
			cv2.putText(img,str(i), (int(np.mean(emoticons[i],0)[0][0]),int(np.mean(emoticons[i],0)[0][1])), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0))
			for j in range(len(emoticons)):
				if emoticons[i] is not emoticons[j]:
					""" Takes the center between the two emoticons. """
					tempSet = list(emoticons[i][0]) + list(emoticons[j][0])
					distance = np.linalg.norm(np.subtract(np.mean(arrows[x],0),np.subtract(np.mean(tempSet),0)))
					""" Associated the two emoticons closest to the arrow as a connection.
					    Whichever emoticon is closer to the center of the arrow than 
					    the center of the bounding box around the arrow is the emoticon
					    being pointing towards, and the other emoticon is being pointed away from.
					"""
					if distance < closestDistance:
						closestNodes = [emoticons[j][0],emoticons[i][0]]
						closestDistance = distance
						if np.linalg.norm(np.subtract(np.mean(emoticons[i][0],0), (rect[0]+(rect[2]/2.0),rect[1]+(rect[3]/2)))) > \
							np.linalg.norm(np.subtract(np.mean(emoticons[i][0],0), (np.mean(arrows[x],0)[0][0],np.mean(arrows[x],0)[0][1]))):
							k = [i,j]
						else:
							k = [j,i]
						

		if len(closestNodes) == 2:
			connections.append(k)

	print "Connected Emoticons:" , connections