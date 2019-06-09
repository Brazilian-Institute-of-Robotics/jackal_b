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
from dynamixel_msgs.msg import JointState
from cv_bridge import CvBridge, CvBridgeError
from std_srvs.srv import Trigger

class camera_client ():

    def __init__(self):
        self.bridge = CvBridge() 
        self.image_sub = rospy.Subscriber("/image_raw",Image,self.callback)
        self.cv_image = None

    def callback(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            #self.gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
            cv2.waitKey(3)
            cv2.namedWindow('cv_image', cv2.WINDOW_NORMAL)
            cv2.imshow('frame',self.cv_image)

        except CvBridgeError as e:
            print(e)

    def call_client_srv(self):
        rospy.wait_for_service('take_picture')
        try:
            take_photo = rospy.ServiceProxy('take_picture', Trigger)
            resp1 = take_photo()
            print resp1.message
            return resp1.success
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

if __name__ == "__main__":

    cam = camera_client()
    rospy.init_node('camera_client', anonymous=True)
    rate = rospy.Rate(1)
    # rospy.spin() # para que sempre fique publicando ou rodando meu programa
    while(not rospy.is_shutdown()):
        cam.call_client_srv()
        rate.sleep()
