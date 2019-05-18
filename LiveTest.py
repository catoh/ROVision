import ImageUtilities as IU
import BlueLine as BL
import cv2
import time

#cap = cv2.VideoCapture(0)

url = "rtsp://888888:rov@192.168.1.2:554/cam/realmonitor?channel=3&subtype=0"

cap = cv2.VideoCapture(url)

width = 1.7

while True:

    ret, frame = cap.read()

    #cv2.imshow("show", frame)

    BL.findCrack(frame, width)

    time.sleep(5)

    if cv2.waitKey(1) & 0xff == 27:
	    break


cap.release()
cv2.destroyAllWindows()


