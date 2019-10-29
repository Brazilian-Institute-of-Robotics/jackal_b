#!/usr/bin/env python

import rospy
import sys
import cv2
import numpy as np
import time
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from math import pi
from std_srvs.srv import *

# this class is responsable for initiating all the variables and methods used in the image capture
class camera_service():

    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()
        self.sub_image = rospy.Subscriber("/image_raw", Image, self.callback) 
        self.cv_image = None
        self.frame = None

    def service(self):
        serv = rospy.Service('take_picture', Trigger, self.take_picture_callback)
        print ("Ready to take a picture.")
        rospy.spin()


    def callback(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            #self.gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
            cv2.waitKey(3)
            #cv2.namedWindow('cv_image', cv2.WINDOW_NORMAL)
            cv2.imshow('frame',self.cv_image)

        except CvBridgeError as e:
            print(e)

    def take_picture_callback(self,req):
         cv2.imwrite('/home/senai/Imagens/aruco2.png', self.cv_image)
         return TriggerResponse(True, "hi")


if __name__ == "__main__":

    rospy.init_node("service", anonymous=True)
    cam = camera_service()
    rate = rospy.Rate(10)
    while(not rospy.is_shutdown()):
        cam.service()
rate.sleep()