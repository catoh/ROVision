import cv2
import numpy as np

def gBlur(img, block_size, count):
    blur = img.copy()
    for _ in range(count):
        blur = cv2.GaussianBlur(blur, (block_size, block_size), 0)
    return blur

def detThreshVal(img):
    thresh_val = 60

    thresh_val = int(np.mean(img))

    return thresh_val

def printContours(contours):
    print("Shape: ", contours.shape, '\n')

def getBlue(img):
    blue = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    BLUE_MIN = np.array([100,150,0], np.uint8)
    BLUE_MAX = np.array([140,255,255], np.uint8)
    blue = cv2.inRange(blue, BLUE_MIN, BLUE_MAX)
    return blue