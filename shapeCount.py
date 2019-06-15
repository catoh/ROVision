# shapeCount should be called with the following format
#   python shapeCount.py PATH_TO_IMAGE


import cv2
import numpy as np
import sys
import ImageUtilities as IU

# detThreshVal() analyzes a grayscale image and returns an appropriate
#   threshold value to distinguish the foreground shapes from the background
def detThreshVal(blurred):
    #thresh_value = 100

    # get the mean value of all the pixels in the image
    thresh_value = int(np.mean(blurred)*0.9)
    #print('Mean pixel value: ', thresh_value)
    
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
    acc = 0.04*peri
    approx = cv2.approxPolyDP(c, acc, True)

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


def countShapes(img):
    count = [0,0,0,0]

    # load the target image
    image = img.copy()

    # convert the image to grayscale to simplify
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur the image to eliminate any artifacts or outlines
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    blurred = cv2.GaussianBlur(blurred, (5,5), 0)
    cv2.imwrite('./Media/blur.jpg', blurred)

    # perform thresholding to separate shapes from background
    #   TODO: test detThreshVal thoroughly
    thresh_value = detThreshVal(blurred)
    ret, thresh = cv2.threshold(blurred, thresh_value, 255, cv2.THRESH_BINARY_INV)    
    cv2.imwrite('./Media/thresh.jpg', thresh)
    

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
            
    # print the result
    #print('   ', count[0], ' triangles,\n   ', count[1], ' squares,\n   ', count[2], ' lines,\n   ', count[3], ' circles\n')
    printOutput(count)

def printOutput(count):
    tricount = str(count[0])
    licount = str(count[1])
    sqcount = str(count[2])
    cicount = str(count[3])

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 5
    font_thicc = 5

    output = np.zeros((900,900,3), np.uint8)   

    output = cv2.line(output, (100,100), (100,200), (0,0,255), 4)
    cv2.putText(output, licount, (200, 200), font, font_size, (0,0,255), font_thicc)

    output = cv2.rectangle(output, (50, 300), (150, 400), (0,0,255), 5)
    cv2.putText(output, sqcount, (200, 400), font, font_size, (0,0,255), font_thicc)

    output = cv2.circle(output, (100, 550), 50, (0,0,255), 4)
    cv2.putText(output, cicount, (200, 600), font, font_size, (0,0,255), font_thicc)

    triangle = np.array([[50,800],[150,800],[100,700]], np.int32)
    #triangle = np.reshape()
    output = cv2.polylines(output, [triangle], True, (0,0,255), 4)
    cv2.putText(output, tricount, (200, 800), font, font_size, (0,0,255), font_thicc)
    
    cv2.imshow("shapes", output)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #if cv2.waitKey(27) & 0xff == 27:
	#    cv2.destroyAllWindows()
