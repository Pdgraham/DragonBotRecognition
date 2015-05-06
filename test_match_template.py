import numpy as np
import argparse
import cv2
"""
Test code that uses OpenCV's matchTemplate to find an emoticon on an image 
	and display the region found
Image and emoticon sizes are not adjusted:
	Test emoticon images are the approximate size of emoticons in the test sheet images 
"""

#python find_emoticon.py --page page.png --emoticon emoticon.png
# EX: python find_emoticon.py --page testimg4.jpg --emoticon 1.png

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--page", required = True,
	help = "Path to the page image")
ap.add_argument("-w", "--emoticon", required = True,
	help = "Path to the emoticon image")
args = vars(ap.parse_args())
 
# load the page and emoticon images
imageColor = cv2.imread(args["page"])
page = cv2.imread(args["page"])
emoticon = cv2.imread("Emojis/" + args["emoticon"])

(emoticonHeight, emoticonWidth) = emoticon.shape[:2]

# find the emoticon in the page
result = cv2.matchTemplate(page, emoticon, cv2.TM_CCOEFF)
(_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)

# grab the bounding box of emoticon and extract it from
# the page image
topLeft = maxLoc
botRight = (topLeft[0] + emoticonWidth, topLeft[1] + emoticonHeight)
roi = page[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]
 
# construct a darkened transparent 'layer' to darken everything
# in the page except for emoticon
mask = np.zeros(page.shape, dtype = "uint8")
page = cv2.addWeighted(page, 0.25, mask, 0.75, 0)

# put the original emoticon back in the image so that he is
# 'brighter' than the rest of the image
page[topLeft[1]:botRight[1], topLeft[0]:botRight[0]] = roi
 
# display the images
cv2.imshow("page", page)
cv2.imshow("emoticon", emoticon)
cv2.waitKey(0)