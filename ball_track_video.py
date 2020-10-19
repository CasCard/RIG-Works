import os
import numpy as np
import cv2
centroids={}

def findRed(img):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower=np.array([0,100,100])
    upper = np.array([10, 255, 255])
    mask=cv2.inRange(imgHSV,lower,upper)
    getContours(mask)
    imS = cv2.resize(mask, (960, 540))
    cv2.imshow("img",imS)

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
            M=cv2.moments(cnt)
            peri = cv2.arcLength(cnt,True)
                #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            objCor = len(approx)
            # print(objCor)
            x, y, w, h = cv2.boundingRect(approx)
            if w>100 and h > 100:
                 Xc = int(M['m10'] / M['m00'])
                 Yc = int(M['m01'] / M['m00'])
                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                 centroids.update({"Centroid": [Xc, Yc]})


path="Videos/ballmotion.m4v"
cap=cv2.VideoCapture(path)

while(cap.isOpened()):
    success,frame=cap.read()
    getContours(frame, edges)
    findRed(frame)
    # re,newResult=cap.read()
	  imS = cv2.resize(frame, (960, 540))
    cv2.imshow('Ball motion',imS)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(centroids)
cap.release()
cv2.destroyAllWindows()
