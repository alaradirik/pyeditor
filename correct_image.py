from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
 

def order_points(points):
	"""
		Initializes a list of coordinates for edge detection.
	"""
	rect = np.zeros((4, 2), dtype = "float32")
 
	# Define top-left and bottom-right points
	s = points.sum(axis = 1)
	rect[0] = points[np.argmin(s)]
	rect[2] = points[np.argmax(s)]
 
	# Calculate the location of top-right and bottom-left points
	diff = np.diff(points, axis = 1)
	rect[1] = points[np.argmin(diff)]
	rect[3] = points[np.argmax(diff)]
 
	return rect

def four_point_transform(image, points):
	"""
		Applies a perspective transform to images.
	"""
	rect = order_points(points)
	(tl, tr, br, bl) = rect
 
	# Calculate the width of the new/corrected image
	width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	max_width = max(int(width_a), int(width_b))
 
	# Calculate the height of the new/corrected image
	height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	max_height = max(int(height_a), int(height_b))
 
	# Transform the image
	dst = np.array([
		[0, 0],
		[max_width - 1, 0],
		[max_width - 1, max_height - 1],
		[0, max_height - 1]], dtype = "float32")
 
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (max_width, max_height))
 
	return warped

def transform_image(image_path):
	# Load and resize the image
	image = cv2.imread(image_path)
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)
	 
	# Convert to grayscale, blur and find the edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)

	# Find the contours of the document/target screne
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	 
	# Approximate the contours and reiterate until the screen is found
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	 
		if len(approx) == 4:
			screenCnt = approx
			break

	# Apply the four point transform using the screen contours
	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
	 
	# Convert the transformed image to grayscale and threshold it
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	
	# Save transformed image
	cv2.imwrite(image_path, warped)
	return