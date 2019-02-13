#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def joy_listener():

    # starts the node
    rospy.init_node("gazebo_joy", anonymous=True) #rue ensures that your node has a unique name by adding random numbers to the end of NAME.

    # subscribe to joystick inputs
    rospy.Subscriber("joy", Joy, tj_callback, queue_size=1)

    # keep node up until ctrl+c is pressed
    rospy.spin()

# called when joy message is received
def tj_callback(data):

    # start publisher of cmd_vel to control the simulation in Gazebo
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

    # Create Twist message & add linear x from left analog and angular z from right analog
    if data.axes[2] == 1:                # button check (LT)
        twist = Twist()
        twist.linear.x = data.axes[1]       # vertical moviment of left analog
        twist.angular.z = data.axes[3]      # horizontal moviment of right analog
    else:  #full speed
        twist = Twist()
        twist.linear.x = 1.5 * data.axes[1]       
        twist.angular.z = 1.5 * data.axes[3]

    # record values to log file and screen
    rospy.loginfo("twist.linear: %f ; angular %f", twist.linear.x, twist.angular.z)

    # process joystick RB button as a enable/disable button
    if data.axes[5] == -1:        # RB button on xbox controller
        
        # publish cmd_vel move command to the /cmd_vel topic
        pub.publish(twist)

if __name__ == '__main__':
    try:
        joy_listener()
    except rospy.ROSInterruptException:
        pass