import numpy as np
import cv2


cap = cv2.VideoCapture(0)

url = "rtsp://888888:rov@192.168.1.2:554/cam/realmonitor?channel=3&subtype=0"

#cap = cv2.VideoCapture(url)

rlvl = 100

x = 213
y = 159

def nothing(x):
	pass

cv2.namedWindow("resbw")
cv2.createTrackbar("LowerAH","resbw",0,255,nothing)
cv2.createTrackbar("UpperAH","resbw",15,255,nothing)
cv2.createTrackbar("LowerAS","resbw",150,255,nothing)
cv2.createTrackbar("UpperAS","resbw",255,255,nothing)
cv2.createTrackbar("LowerAV","resbw",140,255,nothing)
cv2.createTrackbar("UpperAV","resbw",255,255,nothing)

cv2.createTrackbar("LowerBH","resbw",160,255,nothing)
cv2.createTrackbar("UpperBH","resbw",255,255,nothing)
cv2.createTrackbar("LowerBS","resbw",240,255,nothing)
cv2.createTrackbar("UpperBS","resbw",255,255,nothing)
cv2.createTrackbar("LowerBV","resbw",0,255,nothing)
cv2.createTrackbar("UpperBV","resbw",255,255,nothing)

cv2.createTrackbar("LowerCB","resbw",0,255,nothing)
cv2.createTrackbar("UpperCB","resbw",125,255,nothing)
cv2.createTrackbar("LowerCG","resbw",0,255,nothing)
cv2.createTrackbar("UpperCG","resbw",125,255,nothing)
cv2.createTrackbar("LowerCR","resbw",105,255,nothing)
cv2.createTrackbar("UpperCR","resbw",255,255,nothing)



while 1==1:
	ret, frame = cap.read()
	# count = 0
	hsv =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	lowa = np.array([cv2.getTrackbarPos("LowerAH","resbw"),cv2.getTrackbarPos("LowerAS","resbw"),cv2.getTrackbarPos("LowerAV","resbw")])
	uppa = np.array([cv2.getTrackbarPos("UpperAH","resbw"),cv2.getTrackbarPos("UpperAS","resbw"),cv2.getTrackbarPos("UpperAV","resbw")])

	lowb = np.array([cv2.getTrackbarPos("LowerBH","resbw"),cv2.getTrackbarPos("LowerBS","resbw"),cv2.getTrackbarPos("LowerBV","resbw")])
	uppb = np.array([cv2.getTrackbarPos("UpperBH","resbw"),cv2.getTrackbarPos("UpperBS","resbw"),cv2.getTrackbarPos("UpperBV","resbw")])

	lowc = np.array([cv2.getTrackbarPos("LowerCB","resbw"),cv2.getTrackbarPos("LowerCG","resbw"),cv2.getTrackbarPos("LowerCR","resbw")])
	uppc = np.array([cv2.getTrackbarPos("UpperCB","resbw"),cv2.getTrackbarPos("UpperCG","resbw"),cv2.getTrackbarPos("UpperCR","resbw")])

	a_lower_red = lowa
	a_upper_red = uppa

	b_lower_red = lowb
	b_upper_red = uppb

	c_lower_red = lowc
	c_upper_red = uppc

	maska = cv2.inRange(hsv, a_lower_red, a_upper_red)
	maskb = cv2.inRange(hsv, b_lower_red, b_upper_red)  #this will create a binary	 overlay image that lets applicalbe pixels through##
	
	mask = (maska + maskb)

	res1 = cv2.bitwise_and(frame, frame, mask=mask) #image when viewed through the mask

	maskc = cv2.inRange(frame, c_lower_red, c_upper_red)

	res = cv2.bitwise_and(res1, res1, mask=maskc)
	resbw = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)


	#### [y,x]
	q1 = resbw[1:y,1:x]
	q2 = resbw[1:y,x+1:2*x]
	q3 = resbw[1:y,2*x+1:3*x]

	q4 = resbw[y+1:2*y,1:x]
	q5 = resbw[y+1:2*y,x+1:2*x]
	q6 = resbw[y+1:2*y,2*x+1:3*x]

	q7 = resbw[2*y+1:3*y,1:x]
	q8 = resbw[2*y+1:3*y,x+1:2*x]
	q9 = resbw[2*y+1:3*y,2*x+1:3*x]
	

	cv2.imshow("resbw",resbw)

	avg0 = np.mean(resbw)
	avg1 = np.mean(q1)
	avg2 = np.mean(q2)
	avg3 = np.mean(q3)
	avg4 = np.mean(q4)
	avg5 = np.mean(q5)
	avg6 = np.mean(q6)
	avg7 = np.mean(q7)
	avg8 = np.mean(q8)
	avg9 = np.mean(q9)
	avg_arr = [avg1,avg2,avg3,avg4,avg5,avg6,avg7,avg8,avg9]


	for i in (avg_arr):
		if i > 3*avg0:
			print (avg_arr.index(i))

	if cv2.waitKey(1) & 0xff == 27:
		break

	
cap.release()
cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()
