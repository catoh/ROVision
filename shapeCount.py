import cv2
import numpy as np
import sys

def detect(c):
    shape = 'unidentified'
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04*peri, True)
    app_len = len(approx)
    #print('app_len: ', app_len)

    if app_len == 2:
        shape = 'line'
    elif app_len == 3:
        shape = 'triangle'
    elif app_len == 4:
        shape = 'square'
    else:
        shape = 'circle'

    return shape

def countShapes(img_path):
    count = [0,0,0,0]

    image = cv2.imread(img_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('/home/hc/Desktop/ROV-vision/thresh.jpg', thresh)
    
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    #cont_len = len(contours)
    #print('contour_len: ', cont_len)

    for c in contours:
        shape = detect(c)

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

    img_path = str(sys.argv[1])

    count = countShapes(img_path)

    print('   ', count[0], ' triangles,\n   ', count[1], ' squares,\n   ', count[2], ' lines,\n   ', count[3], ' circles\n')
