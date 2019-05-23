# BlueLine includes functions to find a blue rectangle in an image and calculate its
#    length given its width in centimeters


import ImageUtilities as IU
import numpy as np
import cv2
import math

# distance calculates the distance bewteen two points
def distance(point1, point2):
    #print("Point 1: ", point1, "\nPoint 2: ", point2)
    x1, y1 = point1                     # get x and y coordinates from point 1
    x2, y2 = point2                     # get x and y coordinates from point 2
    under = (y2-y1)**2 + (x2-x1)**2
    result = math.sqrt(under)
    return result

# convertApproxToCorners extracts the vertex point tuples from the approximated contour
def convertApproxToCorners(approx):
    corners = []                    
    for i  in range(len(approx)):
        corners.append(approx[i][0])
    return corners

# calcSideLengths constructs an array of lengths of each side of the contour
def calcSideLengths(corners):
    sides = []
    for i in range(-1, len(corners)-1):
        sides.append(distance(corners[i], corners[i+1]))
    return sides

# avgSides finds the average length of the short sides and long sides of the rectangle
def avgSides(sides):
    sides.sort()                            # sort the sides array in ascending length order
    short_side = (sides[0] + sides[1])/2    # average the sort sides
    long_side = (sides[2] + sides[3])/2     # average the long sides
    s_l = (short_side, long_side)           
    return s_l                              # return a tuple of the average side lengths

# calcLength finds the length in centimeters of a rectangle
def calcLength(contour, width):
    peri = cv2.arcLength(contour, True)                     # get the length of the perimeter
    approx = cv2.approxPolyDP(contour, 0.01*peri, True)     # reduce the contour to a set of vertices
    corners = convertApproxToCorners(approx)                # get the points of the corners
    sides = calcSideLengths(corners)                        # get the lengths of the sides
    shrt, lng = avgSides(sides)                             # average the side lengths
    rate = shrt/width                                       # calculate the pixel to centimeter ratio
    length = lng/rate                                       # convert the pixel length to centimeters
    length = length + 1                                     # add 1 cm to correct for bias
    return length

# findCrack finds a blue rectangle in the image and returns the length of the rectangle in centimeters
def findCrack(img, width):

    #img_path = './Media/small.jpg'

    #img = cv2.imread(img_path)
    blue = img.copy()            

    blue = IU.gBlur(blue, 5, 1)                 # blur image
    #cv2.imwrite('./Media/blur.jpg', blue)

    blue = IU.getBlue(blue)                     # extract blue
    #cv2.imwrite('./Media/blue.jpg', blue)

    ret, contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # find the outline of the blue shape
    #cv2.drawContours(img, contours, -1, (0,255,0), 5)
    #cv2.imwrite('./Media/contours.jpg', img)

    #width = 1.7
    for c in contours:
        length = calcLength(c, width)       # find the length of the shape
        print('Length: ', length)