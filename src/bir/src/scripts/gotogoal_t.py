#!/usr/bin/python

import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

class MoveTo():

    def __init__(self, odom_topic, cmd_vel_topic, tolerance=0.1):
        # Internal Variables
        self._odomTopic = odom_topic
        self._cmd_velTopic = cmd_vel_topic
        self._tolerance = tolerance
        self._poseTarget = [0, 0]
        self._pose = [0, 0, 0]
        self._pi = 3.141592
        #self._angularVelocityPID = PID(1, 0, 0, 0.1)
        self._end = False
        self._odomRecived = False
        # Setting Odom Subscriber
        self._odomSubscriber = rospy.Subscriber(odom_topic, Odometry, self.odomCallback)
        whileRate = rospy.Rate(0.5)
        while (not rospy.is_shutdown()) and (not self._odomRecived):
            whileRate.sleep()
        if(self._odomRecived):
            rospy.loginfo("Odom Topic Connected")
        # Setting Goals Subscribers
        self._goalPoseSubscriber = rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.goalPoseCallback)
        self._goalPointSubscriber = rospy.Subscriber("/typea/goal_point", Point, self.goalPointCallback)
        # Setting Cmd Vel Publisher
        self._cmd_velPub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    def odomCallback(self, msg):
        if (not self._odomRecived):
            self._odomRecived = True
            self._poseTarget[0] = msg.pose.pose.position.x
            self._poseTarget[1] = msg.pose.pose.position.y
        
        self._pose[0] = msg.pose.pose.position.x
        self._pose[1] = msg.pose.pose.position.y
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        _, _, self._pose[2] = euler_from_quaternion(orientation_list)
    
    def goalPoseCallback(self, msg):
        self.goTo(msg.pose.pose.position.x, msg.pose.pose.position.y)
        rospy.loginfo("Goal Recived: " + str(self._poseTarget[0]) + "," + str(self._poseTarget[1]))

    def goalPointCallback(self, msg):
        self.goTo(msg.x, msg.y)
        rospy.loginfo("Goal Recived: " + str(self._poseTarget[0]) + "," + str(self._poseTarget[1]))

    def goTo(self, x, y):
        self._poseTarget[0] = x
        self._poseTarget[1] = y

    def run(self):
        velocityCommand = Twist()
        velocityCommand.linear.x = 0.5
        distanceToTarget = math.sqrt((self._poseTarget[0] - self._pose[0])**2 + (self._poseTarget[1] - self._pose[1])**2)
        if(distanceToTarget <= self._tolerance):
            self._end = True
            velocityCommand.angular.z = 0
            velocityCommand.linear.x = 0
        else :
            desiredAngle = math.atan2((self._poseTarget[1] - self._pose[1]), (self._poseTarget[0] - self._pose[0]))
            erroAngle = (desiredAngle - (self._pose[2]))
            velocityCommand.angular.y = erroAngle
            if(erroAngle > self._pi): 
                erroAngle -= (2*(self._pi))
            elif (erroAngle < -self._pi): 
                erroAngle += (2*(self._pi))
            velocityCommand.angular.z = erroAngle
        
        self._cmd_velPub.publish(velocityCommand)

if __name__ == "__main__":
    rospy.init_node("moveTo_python")
    moveTo = MoveTo("/typea/position", "/typea/cmd_vel", 0.05)
    whileRate = rospy.Rate(10)
    
    while(not rospy.is_shutdown()):
        moveTo.run()
whileRate.sleep()