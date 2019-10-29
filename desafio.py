#!/usr/bin/env python

import rospy
import sys
import cv2
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dynamixel_msgs.msg import JointState

# this class is responsable for initiating all the variables and methods used in the movement
class motor_movement():

    def __init__(self):

        # subscribers to pan and tilt information topics
        self.motor1_sub = rospy.Subscriber("/joint3_controller/state", JointState, self.motor1_callback)
        self.motor2_sub = rospy.Subscriber("/joint4_controller/state", JointState, self.motor2_callback)

        # starts publishers of joint controllers topics to control the Dynamixels
        self.motor1_pub = rospy.Publisher("/joint3_controller/command", Float64, queue_size=10)          # motor1
        self.motor2_pub = rospy.Publisher("/joint4_controller/command", Float64, queue_size=10)         #  motor2

        # initial variables
        self.motor1_position = 0
        self.motor2_position = 0
        self.motor1_is_moving = False
        self.motor2_is_moving = False

    # callback method por the pan motor
    def motor1_callback(self, msg):
        self.motor1_position = msg.current_pos
        self.motor1_is_moving = msg.is_moving
    
    #callback method for the tilt motor
    def motor2_callback(self, msg):
        self.motor2_position = msg.current_pos
        self.motor2_is_moving = msg.is_moving

    # method for returning the instant pan position
    def get_motor1_position(self):
        return self.motor1_position

    # method for returning the instant tilt position
    def get_motor2_position(self):
        return self.motor2_position

    # method for returning if the pan motor is moving
    def get_motor1_is_moving(self):
        return self.motor1_is_moving

    # method for returning if the tilt motor is moving
    def get_motor2_is_moving(self):
        return self.motor2_is_moving
        
    # method to publish the goal points into the topics that control the motors        
    def pub_movement(self, motor1, motor2):
        self.motor1_pub.publish(motor1)
        self.motor2_pub.publish(motor2)


# this is the general for controlling all movements and image captures
class image():

    def __init__(self):

        #self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
        #self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.cap = cv2.VideoCapture(0)

    def capture(self):
        self.m_v = motor_movement()

        # Variable of image
        frame = self.cap()
        # Converting to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Using the dictionary of arucos
        res = cv2.aruco.detectMarkers(gray, dictionary)
        # Logic to not send empty values
        if len(res[0]) > 0:
            cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])
            #logic to reconize

            if res[1][0] == 1:
                self.m_v.pub_movement(1,-1)
            

    cv2.namedWindow('cv_image', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',cv_image)
    
    cv2.waitKey(3)


def main():
    im = image()
    # starts the node for the motor movements
    rospy.init_node("pan_tilt", anonymous=True)

    rospy.spin()

if __name__ == "__main__":
    main()