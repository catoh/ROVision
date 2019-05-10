import ImageUtilities as IU
import numpy as np
import cv2
import math

def distance(point1, point2):
    print("Point 1: ", point1, "\nPoint 2: ", point2)
    x1, y1 = point1
    x2, y2 = point2
    under = (y2-y1)**2 + (x2-x1)**2
    result = math.sqrt(under)
    return result

def convertApproxToCorners(approx):
    corners = []
    for i  in range(len(approx)):
        corners.append(approx[i][0])
    return corners

def calcSideLengths(corners):
    sides = []
    for i in range(-1, len(corners)-1):
        sides.append(distance(corners[i], corners[i+1]))
    return sides

def avgSides(sides):
    sides.sort()
    short_side = (sides[0] + sides[1])/2
    long_side = (sides[2] + sides[3])/2
    s_l = (short_side, long_side)
    return s_l

def calcLength(contour, width):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.01*peri, True)
    corners = convertApproxToCorners(approx)
    sides = calcSideLengths(corners)
    shrt, lng = avgSides(sides)
    rate = shrt/width
    length = lng/rate
    return length

img_path = './Media/medium.jpg'

img = cv2.imread(img_path)
blue = img.copy()

blue = IU.gBlur(blue, 5, 1)
cv2.imwrite('./Media/blur.jpg', blue)

blue = IU.getBlue(blue)
cv2.imwrite('./Media/blue.jpg', blue)

ret, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0,255,0), 5)
cv2.imwrite('./Media/contours.jpg', img)

width = 1.7
for c in contours:
    length = calcLength(c, width)
    print('Length: ', length)