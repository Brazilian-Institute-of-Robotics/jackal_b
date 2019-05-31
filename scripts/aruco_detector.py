#!/usr/bin/env python

import sys
import rospy
#sys.path.append("/usr/local/lib/python2.7/dist-packages")
#sys.path.append("./.local/lib/python2.7/site-packages")
#sys.path.append("./.local/lib/python3.5/site-packages")
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sys

class aruco:
    def __init__ (self):

        rospy.init_node("aruco", anonymous=True)
        self.cap = cv2.VideoCapture(0)
        #self.bridge = CvBridge()
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.frame = None
        #self.pub_image = rospy.Publisher("/image_raw", self.frame, queue_size=10)  
        #self.image_sub = rospy.Subscriber("/image_raw",Image,self.callback)

    def image_camera (self):
        self.ret, self.frame = self.cap.read()
        cv2.imshow('frame',self.frame)

    def capture_image (self):

        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.res = cv2.aruco.detectMarkers(self.gray, self.dictionary)
        if len(self.res[0]) > 0:
            cv2.aruco.drawDetectedMarkers(self.frame,self.res[0],self.res[1])
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame',self.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.spin()
       

if __name__ == "__main__":
    aru = aruco()
    whileRate = rospy.Rate(50)
    while(not rospy.is_shutdown()):
        aru.image_camera()
        aru.capture_image()
       # aru.convertion()
       # aru.detect_aruco()
        whileRate.sleep()
    #%%

