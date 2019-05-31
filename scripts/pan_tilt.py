#!/usr/bin/env python

import rospy
import sys
import cv2
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dynamixel_msgs.msg import JointState
from cv_bridge import CvBridge, CvBridgeError
from math import pi

# this class is responsable for initiating all the variables and methods used in the movement
class motor_movement():

    def __init__(self):

        # subscribers to pan and tilt information topics
        self.pan_sub = rospy.Subscriber("/joint3_controller/state", JointState, self.pan_callback)
        self.tilt_sub = rospy.Subscriber("/joint4_controller/state", JointState, self.tilt_callback)

        # starts publishers of joint controllers topics to control the Dynamixels
        self.pub_pan = rospy.Publisher("/joint3_controller/command", Float64, queue_size=10)          # panning motor
        self.pub_tilt = rospy.Publisher("/joint4_controller/command", Float64, queue_size=10)         # tilting motor

        # initial variables
        self.pan_position = 0
        self.tilt_position = 0
        self.pan_is_moving = False
        self.tilt_is_moving = False

    # callback method por the pan motor
    def pan_callback(self, msg):
        self.pan_position = msg.current_pos
        self.pan_is_moving = msg.is_moving
    
    #callback method for the tilt motor
    def tilt_callback(self, msg):
        self.tilt_position = msg.current_pos
        self.tilt_is_moving = msg.is_moving

    # method for returning the instant pan position
    def get_pan_position(self):
        return self.pan_position

    # method for returning the instant tilt position
    def get_tilt_position(self):
        return self.tilt_position

    # method for returning if the pan motor is moving
    def get_pan_is_moving(self):
        return self.pan_is_moving

    # method for returning if the tilt motor is moving
    def get_tilt_is_moving(self):
        return self.tilt_is_moving
        
    # method to publish the goal points into the topics that control the motors        
    def pub_movement(self, pan, tilt):
        self.pub_pan.publish(pan)
        self.pub_tilt.publish(tilt)


# this is the general for controlling all movements and image captures
class image_capture():

    def __init__(self):
        self.mm = motor_movement()
        self.pan_moving = self.mm.get_pan_is_moving()
        self.tilt_moving = self.mm.get_tilt_is_moving()
        self.tilt = self.mm.get_tilt_position()
        self.bridge = CvBridge()
        self.cv_image = None
        self.image_sub = rospy.Subscriber("/image_raw",Image,self.callback)

    def callback(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def save_image(self, x, y):
        cv2.imwrite('/home/leo5on/Pictures/pan_tilt_test/image_' + str(x) + str(y) + '.jpeg', self.cv_image)

    # method responsable for publishing the goal points for the movement
    def movement(self):
        h = "hori"
        inc = "incli"
        rospy.sleep(1)
        self.mm.pub_movement(0,0)
        rospy.sleep(7)
        for i in range (0, 4):
            self.save_image(i, h)
            rospy.sleep(1)
            self.mm.pub_movement((i*pi/2), (-pi/4))
            rospy.sleep(2)
            self.save_image(i, inc)
            rospy.sleep(1)
            self.mm.pub_movement(((i+1)*pi/2), 0)
            rospy.sleep(2)

def main():

    # starts the node for the motor movements
    rospy.init_node("pan_tilt", anonymous=True)
    ic = image_capture()

    ic.movement()

    rospy.spin()

if __name__ == "__main__":
    main()