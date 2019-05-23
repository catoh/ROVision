# Image Utilities includes some functions to aid in image recognition

import cv2
import numpy as np


# gBlur performs a gaussian blur on an image multiple times
def gBlur(img, block_size, count):
    blur = img.copy()
    for _ in range(count):
        blur = cv2.GaussianBlur(blur, (block_size, block_size), 0)
    return blur

# detThrechVal finds the mean pixel value of an image for use in thresholding
def detThreshVal(img):
    thresh_val = 60

    thresh_val = int(np.mean(img))

    return thresh_val


def printContours(contours):
    print("Shape: ", contours.shape, '\n')

# getBlue converts an image to HSV and extracts any blue pixels from the image
def getBlue(img):
    blue = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    BLUE_MIN = np.array([100,150,0], np.uint8)
    BLUE_MAX = np.array([140,255,255], np.uint8)
    blue = cv2.inRange(blue, BLUE_MIN, BLUE_MAX)
    return blue