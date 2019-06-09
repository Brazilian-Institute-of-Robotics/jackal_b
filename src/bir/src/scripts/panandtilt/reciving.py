#!/usr/bin/env python

import sys
import numpy as np
import cv2
import sys
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Bool

class reciving ():

    def __init__(self):
        self.bridge = CvBridge() 
        self.image_sub = rospy.Subscriber("/image_raw",Image,self.callback)
        self.cv_image = None

    def callback(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
            cv2.waitKey(3)
            #cv2.namedWindow('cv_image', cv2.WINDOW_NORMAL)
            cv2.imshow('frame',self.gray)

        except CvBridgeError as e:
            print(e)
if __name__ == "__main__":
    rec = reciving()
    rospy.init_node('recive', anonymous=True)
    whileRate = rospy.Rate(1)
    rospy.spin() # para que sempre fique publicando ou rodando meu programa
    while(not rospy.is_shutdown()):
        rec.callback()


