#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
from dynamixel_msgs.msg import JointState
from math import pi

class joy_motor():

    def __init__(self):

        # starts the node
        rospy.init_node("joy_motor", anonymous=True)

        # subscriber to joystick inputs
        self.joy = rospy.Subscriber("joy", Joy, self.get_joy_commands, queue_size=1)

        # subscribers to pan and tilt positions topics
        self.pan_sub = rospy.Subscriber("/pan_controller/state", JointState, self.get_pan_position_motor)
        self.tilt_sub = rospy.Subscriber("/tilt_controller/state", JointState, self.get_tilt_position_motor)

        # starts publishers of joint controllers topics to control the Dynamixels
        self.pub_pan = rospy.Publisher("/pan_controller/command", Float64, queue_size=1)          # panning motor
        self.pub_tilt = rospy.Publisher("/tilt_controller/command", Float64, queue_size=1)         # tilting motor

        # initial variables 
        self.pan_position = 0
        self.tilt_position = 0
        self.pan = 0
        self.tilt = 0

    # this function is responsable for getting the current position of the pan motor
    def get_pan_position_motor(self, msg):
        self.pan_position = msg.current_pos

    # this function is responsable for getting the current position of the pan motor
    def get_tilt_position_motor(self, msg):
        self.tilt_position = msg.current_pos

    # this function is responsable for reading the joystick inputs
    def get_joy_commands(self, data):
        self.pan = data.axes[3]                             # horizontal movement right analog
        self.tilt = data.axes[1]                            # vertical movement of left analog

    # this function is responsable for the increment calculation for the fluid movement and publishing the commands
    def increment(self):
        pan_go = self.pan_position + (0.3*self.pan)
        tilt_go = self.tilt_position + (0.3*self.tilt)
        self.pub_pan.publish(pan_go)
        self.pub_tilt.publish(tilt_go)


# main code of the script 
def main():
    move = joy_motor()
    whileRate = rospy.Rate(10)

    while (not rospy.is_shutdown()):
        move.increment()
        whileRate.sleep()

if __name__ == '__main__':
    main()