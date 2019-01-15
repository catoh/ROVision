# shapeCount should be called with the following format
#   python shapeCount.py PATH_TO_IMAGE


import cv2
import numpy as np
import sys

# detThreshVal() anazlyzes a grayscale image and returns an appropriate
#   threshold value to distinguish the foreground shapes from the background
def detThreshVal(blurred):
    thresh_value = 60
    thresh_value = int(np.mean(blurred))
    print('Mean pixel value: ', thresh_value)
    return thresh_value

# detect() takes a single opencv contour and returns the shape
#   of the contour as a string 
def detect(c):

    # initialize shape as unidentified, if detect() ever returns this
    #   string then something has gone wrong
    shape = 'unidentified'

    # get the contour perimeter
    peri = cv2.arcLength(c, True)

    # approxPolyDP returns the vertices of the given contour shape
    approx = cv2.approxPolyDP(c, 0.04*peri, True)

    # get the number of vertices
    app_len = len(approx)
    #print('app_len: ', app_len)


    # determine shape based on the number of vertices
    if app_len == 2:
        shape = 'line'
    elif app_len == 3:
        shape = 'triangle'
    elif app_len == 4:
        shape = 'square'
    else:
        shape = 'circle'

    # return
    return shape

def countShapes(img_path):
    count = [0,0,0,0]

    # load the target image
    image = cv2.imread(img_path)

    # convert the image to grayscale to simplify
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur the image to eliminate any artifacts or outlines
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    blurred = cv2.GaussianBlur(blurred, (5,5), 0)
    # perform thresholding to separate shapes from background
    #   TODO: devise a method to determine an appropriate thresh_value for an
    #         arbitrary image, hard-coding this value is extremely unreliable
    thresh_value = detThreshVal(blurred)
    ret, thresh = cv2.threshold(blurred, thresh_value, 255, cv2.THRESH_BINARY_INV)    
    cv2.imwrite('/home/hc/Github/ROVision/Media/thresh.jpg', thresh)
    
    # get outline of the shapes
    #   findcontours returns a list of numpy arrays containing the coordinates of the boundaries
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    #cont_len = len(contours)
    #print('contour_len: ', cont_len)

    # for each contour in the list
    for c in contours:

        # determine the shape of the contour
        shape = detect(c)

        # increment the appropriate count
        if shape == 'triangle':
            count[0] = count[0] + 1
        elif shape == 'square':
            count[1] = count[1] + 1
        elif shape == 'line':
            count[2] = count[2] + 1
        elif shape == 'circle':
            count[3] = count[3] + 1
        else:
            print("Something went wrong in detect()")

    return count

if __name__ == '__main__':

    # get the image path from the command line arguments
    img_path = str(sys.argv[1])

    # count the shapes
    count = countShapes(img_path)

    # print the result
    print('   ', count[0], ' triangles,\n   ', count[1], ' squares,\n   ', count[2], ' lines,\n   ', count[3], ' circles\n')
