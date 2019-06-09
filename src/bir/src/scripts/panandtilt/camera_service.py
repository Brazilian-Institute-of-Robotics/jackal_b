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
from math import pi
from std_srvs.srv import *

# this class is responsable for initiating all the variables and methods used in the image capture
class camera_service():

    def __init__(self):

        self.ok = False
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()
        self.frame = None
        self.pub_image = rospy.Publisher("/image_raw", Image, queue_size=10) 
        self.service()
    def service(self):
        serv = rospy.Service('take_picture', Trigger, self.take_picture_callback)
        print ("Ready to take a picture.")
        rospy.spin()
   
    def cap_image(self):
        ret, self.frame = self.cap.read()

    def conversion(self):
        try:
            cv_image = self.bridge.cv2_to_imgmsg(self.frame, "bgr8")
            self.pub_image.publish(cv_image)
        except CvBridgeError as e:
            print(e)
    def take_picture_callback(self,req):
         cv2.imwrite('/home/fredlaranja/Pictures/image.png', self.frame)
         return TriggerResponse(True, "hi")


if __name__ == "__main__":

    rospy.init_node("service", anonymous=True)
    cam = camera_service()
    rate = rospy.Rate(10)
    while(not rospy.is_shutdown()):
        cam.cap_image()
        cam.conversion()
        rate.sleep()