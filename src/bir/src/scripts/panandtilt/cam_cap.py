
#!/usr/bin/env python

import rospy
import sys
import cv2
import numpy as np
import time
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dynamixel_msgs.msg import JointState
from cv_bridge import CvBridge, CvBridgeError
from math import pi
#from std_msgs.msg import Bool

class camera():
    
    def __init__(self):
    
         
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()
        self.frame = None
        self.pub_image = rospy.Publisher("/image_raw", Image, queue_size=10)  

    def cap_image(self):
        ret, self.frame = self.cap.read()

    def callback(self):
        try:
            cv_image = self.bridge.cv2_to_imgmsg(self.frame, "bgr8")
            self.pub_image.publish(cv_image)
        except CvBridgeError as e:
            print(e)


if __name__ == "__main__":

    rospy.init_node("motor_movement", anonymous=True)
    cam = camera()
    whileRate = rospy.Rate(50)
    while(not rospy.is_shutdown()):
        cam.cap_image()
        cam.callback()
whileRate.sleep()



