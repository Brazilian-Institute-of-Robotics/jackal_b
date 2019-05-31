#!/usr/bin/env python

import sys
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class aruco:
    def __init__ (self):

        rospy.init_node("aruco", anonymous=True)
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.frame = None
        self.pub_image = rospy.Publisher("/image_raw", Image, queue_size=10)  
        #self.image_sub = rospy.Subscriber("/image_raw",Image,self.callback)


    def image_camera (self):

        ret, self.frame = self.cap.read()
        # cv2.imshow('frame',self.frame)
    def aruco_detector(self):
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.res = cv2.aruco.detectMarkers(self.gray, self.dictionary)
        if len(self.res[0]) > 0:
            cv2.aruco.drawDetectedMarkers(self.frame,self.res[0],self.res[1])
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.imshow('frame',self.frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            rospy.spin()
       
    def conversion(self):
        try:
            cv_image = self.bridge.cv2_to_imgmsg(self.frame, "bgr8")
            self.pub_image.publish(cv_image)
        except CvBridgeError as e:
            print(e)

if __name__ == "__main__":
    aru = aruco()
    whileRate = rospy.Rate(50)
    while(not rospy.is_shutdown()):
        aru.image_camera()
        aru.aruco_detector()
        aru.conversion()
        whileRate.sleep()
    #%%

