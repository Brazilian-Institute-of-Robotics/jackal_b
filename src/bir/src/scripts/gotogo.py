#!/usr/bin/env python
import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion


class Warthog():

    def __init__(self, odom_topic, cmd_vel_topic, tolerance=0.1):
        # Creates a node with name 'warthog_controller' and make sure it is a unique node (using anonymous=True).
        rospy.init_node('warthog_controller', anonymous=True)

        # Publisher which will publish to the topic '/cmd_vel'.
        self.velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        # Subscriber to the Odom data:
        self._odomSubscriber = rospy.Subscriber("/odometry/filtered", Odometry, self.get_position_odom)

        # Internal Variables iniciation
        self._odomTopic = odom_topic
        self._cmd_velTopic = cmd_vel_topic
        self._tolerance = tolerance
        self._pose = [0, 0, 0]
        self.goal_pose = [0, 0]
        self._end = False

        # Gets the inputs from the user
        self.goal_pose[0] = input("Set your x goal: ")
        self.goal_pose[1] = input("Set your y goal: ")

    # Function that converts the Odometry data to Pose type msg
    def get_position_odom(self, msg):
        self._pose[0] = msg.pose.pose.position.x
        self._pose[1] = msg.pose.pose.position.y
        rot_q = msg.pose.pose.orientation #just taking the z orientation
        _, _, self._pose[2] = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

    # Function to move the robot
    def move2goal(self):
        if (not self._end):
            velocityCommand = Twist()
            velocityCommand.linear.x = 0.5
            # Calculation of the distance between the two points
            distance = math.sqrt((self.goal_pose[0] - self._pose[0])**2 + (self.goal_pose[1] - self._pose[1])**2)
            if(distance <= self._tolerance):
                self._end = True
                velocityCommand.angular.z = 0
                velocityCommand.linear.x = 0
            else :
                teta = math.atan2((self.goal_pose[1] - self._pose[1]), (self.goal_pose[0] - self._pose[0]))
                erroAngle = (teta - self._pose[2])
                if(erroAngle > 3.1415):
                    erroAngle -= 2*3.1415
                elif(erroAngle < -3.1415):
                    erroAngle += 2*3.1415
                velocityCommand.angular.z = erroAngle * 0.5
        
            self.velocity_publisher.publish(velocityCommand)



if __name__ == "__main__":
    warthog = Warthog("/odometry/filtered", "/cmd_vel", 0.05)
    whileRate = rospy.Rate(10)
    
    while(not rospy.is_shutdown()):
        warthog.move2goal()
whileRate.sleep()