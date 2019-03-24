import numpy as np
import cv2



#url = "rtsp://888888:rov@192.168.1.2:554/cam/realmonitor?channel=3&subtype=0"
cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

rlvl = 100
initial = 10
go = "error"

nav_arr=[0,0,0,0]
go_arr=[0,0,0,0]
english = ["up","down","left","right"]

x = 213
y = 159

def nothing(x):
	pass

cv2.namedWindow("resbw")
cv2.createTrackbar("LowerAH","resbw",0,255,nothing)
cv2.createTrackbar("UpperAH","resbw",16,255,nothing)
cv2.createTrackbar("LowerAS","resbw",57,255,nothing)
cv2.createTrackbar("UpperAS","resbw",255,255,nothing)
cv2.createTrackbar("LowerAV","resbw",145,255,nothing)
cv2.createTrackbar("UpperAV","resbw",255,255,nothing)

cv2.createTrackbar("LowerBH","resbw",130,255,nothing)
cv2.createTrackbar("UpperBH","resbw",255,255,nothing)
cv2.createTrackbar("LowerBS","resbw",48,255,nothing)
cv2.createTrackbar("UpperBS","resbw",255,255,nothing)
cv2.createTrackbar("LowerBV","resbw",0,255,nothing)
cv2.createTrackbar("UpperBV","resbw",255,255,nothing)

cv2.createTrackbar("LowerCB","resbw",0,255,nothing)
cv2.createTrackbar("UpperCB","resbw",197,255,nothing)
cv2.createTrackbar("LowerCG","resbw",0,255,nothing)
cv2.createTrackbar("UpperCG","resbw",198,255,nothing)
cv2.createTrackbar("LowerCR","resbw",110,255,nothing)
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
	q0 = resbw[1:y,1:x]
	q1 = resbw[1:y,x+1:2*x]
	q2 = resbw[1:y,2*x+1:3*x]

	q3 = resbw[y+1:2*y,1:x]
	q4 = resbw[y+1:2*y,x+1:2*x]
	q5 = resbw[y+1:2*y,2*x+1:3*x]

	q6 = resbw[2*y+1:3*y,1:x]
	q7 = resbw[2*y+1:3*y,x+1:2*x]
	q8 = resbw[2*y+1:3*y,2*x+1:3*x]
	

	cv2.imshow("resbw",resbw)
	cv2.imshow("frame",frame)

	avgt = np.mean(resbw)  ### each avg(n) is set to the avg grey value of section n. avgt is the average of the image
	avg0 = np.mean(q0)
	avg1 = np.mean(q1) #up 
	avg2 = np.mean(q2)
	avg3 = np.mean(q3) #left
	avg4 = np.mean(q4) #mid
	avg5 = np.mean(q5) #right
	avg6 = np.mean(q6)
	avg7 = np.mean(q7) #down
	avg8 = np.mean(q8)


	##

	if avg4 > 3*avgt:  ###this sets a value to 1 if the center section of the screen meets a red threshold
		mid = 1
	else:
		mid = 0

	n=0

	for i in (q1,q7,q3,q5):     ###this sets up,down,left,right sections of an array (nav_arr) to 1 if red threshold is met
		if np.mean(i) > 3*avgt:
			nav_arr[n]=1
		else:
			nav_arr[n]=0
		n+=1


	if (initial > 1):   		#this tree last for the # of times set in "initial"(to compensate for all zero value start)
		if nav_arr[0] == 1:  	#the go array has one of it's four values (up,down,left,right) based off the navigation array
			go_arr[0] = 1
		elif nav_arr[1] == 1:
			go_arr[1] = 1
		elif nav_arr[2] == 1:
			go_arr[2] = 1
		elif nav_arr[3] == 1:
			go_arr[3] = 1
		initial -= initial

	if mid = 0:                 ###mid point boolean will be used to report lateral and horizontal drifting
		print ("drifting")


##### the following section will check the location of the navigation array for the 1 value in the go array
#####if different, the go array has it's value changed based off of what value is in the other axis in the nav array


	if (nav_arr[go_arr.index(1)] != 1) and mid = 1:   

		if (go_arr[0] == 1 or go_arr[1] ==1) and (nav_arr[2] ==1 or nav_arr[3] ==1):
			if nav_arr[2] ==1:
				go_arr[2] =1
			elif nav_arr[3]==1:
				go_arr[3]=1
			go_arr[0] = 0
			go_arr[1] = 0

		if (go_arr[2] == 1 or go_arr[3] ==1) and (nav_arr[0] ==1 or nav_arr[1] ==1):
			if nav_arr[0] ==1:
				go_arr[0] =1
			elif nav_arr[1]==1:
				go_arr[1]=1
			go_arr[2] = 0
			go_arr[3] = 0			

	

	print(go_arr,nav_arr,initial)
	print(english[go_arr.index(1)])


	#out.write(frame)


	if cv2.waitKey(1) & 0xff == 27:
		break
	
cap.release()
cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()
