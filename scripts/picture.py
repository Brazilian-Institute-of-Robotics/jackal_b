#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import Float64
from std_msgs.msg import String

class take:
    def __init__ (self):
        rospy.init_node("photo",anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
        self.cv_image = None
    def callback(self, data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
    def image_show(self):
        cv2.imshow('frame',self.cv_image)
        print(self.cv_image)
        # cv2.waitKey(0)

if __name__ == "__main__":
    t = take()
    whileRate = rospy.Rate(50)
    while(not rospy.is_shutdown()):
        t.image_show()
       #t.callback() NÃO SE CHAMA O CALLBACK AQUI, POIS ELE SEMPRE SERA CHAMADO QUANDO ALGO FOR PUBLICADO NO TOPICO/CAMERARAW
        whileRate.sleep()
    #%%
