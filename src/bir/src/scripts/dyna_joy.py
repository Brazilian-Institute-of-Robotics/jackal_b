#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
from dynamixel_msgs.msg import JointState
from math import pi

class pantilt ():
    
    def __init__(self):

    # starts the node
        rospy.init_node("dyna_joy", anonymous=True)

        # subscriber to joystick inputs
        self.joy = rospy.Subscriber("joy", Joy, self.joy_cmd, queue_size=1)

        # subscribers to pan and tilt positions topics
        # Tópicos para pegar a posição exata do motor
        self.pan_sub = rospy.Subscriber("/pan_controller/state", JointState, self.get_pose_pan)
        self.tilt_sub = rospy.Subscriber("/tilt_controller/state", JointState, self.get_pose_tilt)

        # starts publishers of joint controllers topics to control the Dynamixels
        # Tópicos para publicar a posição para os motores
        self.pub_pan = rospy.Publisher("/pan_controller/command", Float64, queue_size=1)          # panning motor
        self.pub_tilt = rospy.Publisher("/tilt_controller/command", Float64, queue_size=1)         # tilting motor

        # initial variables 
        self.pan_position = 0
        self.tilt_position = 0
        self.pan = 0
        self.tilt = 0
        # msg.corrent_pose is from dynamixel_msgs.
    def get_pose_pan(self, msg):
        self.pan_position = msg.current_pos
    def get_pose_tilt (self, msg):
        self.tilt_position = msg.current_pos 

    def joy_cmd(data,self):
        #ver qual é a posição na lista
        self.pan == data.axes[0]
        self.tilt == data.axes[3] 
    
    def mov(self):
        pan_mov = self.pan_position + (0.1*self.pan)
        tilt_mov = self.tilt_position + (0.1*self.tilt)
        self.pub_pan.publish(pan_mov) #publishing on topic
        self.pub_tilt.publish(tilt_mov)

def main():
    move = pantilt()
    whileRate = rospy.Rate(10)

    while (not rospy.is_shutdown()):
        move.mov()
        whileRate.sleep()

if __name__ == '__main__':
    main()

