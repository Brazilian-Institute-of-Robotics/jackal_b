#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
class pantilt ():
    def joy_listener(self):

    # starts the node
        rospy.init_node("dyna_joy", anonymous=True)

        # subscriber to joystick inputs
        self.joy = rospy.Subscriber("joy", Joy, self.get_joy_commands, queue_size=1)

        # subscribers to pan and tilt positions topics
        # Tópicos para pegar a posição exata do motor
        self.pan_sub = rospy.Subscriber("/joint3_controller/state", JointState, self.get_pan_position_motor)
        self.tilt_sub = rospy.Subscriber("/joint4_controller/state", JointState, self.get_tilt_position_motor)

        # starts publishers of joint controllers topics to control the Dynamixels
        # Tópicos para publicar a posição para os motores
        self.pub_pan = rospy.Publisher("/joint3_controller/command", Float64, queue_size=1)          # panning motor
        self.pub_tilt = rospy.Publisher("/joint4_controller/command", Float64, queue_size=1)         # tilting motor

        # initial variables 
        self.pan_position = 0
        self.tilt_position = 0
        self.pan = 0
        self.tilt = 0
        # msg.corrent_pose is from dynamixel_msgs.
    def get_pose_pan(self,msg):
        self.pan_position = msg.corrent_pose #rads
    def get_pose_tilt (self,msg):
        self.tilt_position = msg.corrent_pose #rads

    def joy_cmd(data,self):
        #ver qual é a posição na lista
        data.axes[x] == self.pan
        data.axes[x] == self.tilt
    
    def mov(self):
        pan_mov = self.pan_position + (0.1*self.pan)
        tilt_mov = self.tilt_position + (0.1*self.tilt)
        self.pub_pan.publish(pan_mov) #publishing on topic
        self.pub_tilt.publish(tilt_mov)

