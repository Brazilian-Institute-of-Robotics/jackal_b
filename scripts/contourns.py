import sys
#sys.path.append("/usr/local/lib/python2.7/dist-packages")
#sys.path.append("./.local/lib/python2.7/site-packages")
sys.path.append("./.local/lib/python3.5/site-packages")
import numpy as np
import cv2
import sys
cap = cv2.VideoCapture(0)
while True:

    _, frame = cap.read()
    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('frame',thresh)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break