#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from math import pow, atan2, sqrt
from tf.transformations import euler_from_quaternion
from std_srvs.srv import Trigger
from geometry_msgs.msg import Point
class Jackal():

    def __init__(self, odom_topic, cmd_vel_topic, tolerance):
        # Creates a node with name 'jackal' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('jackal', anonymous=True)

        # Publisher which will publish to the topic '/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/cmd_vel',
                                                  Twist, queue_size=10)

        #location with odometry
        self._odomSubscriber = rospy.Subscriber("/odometry/filtered", 
                                                Odometry, self.get_position_odom)

        # Subscriber from aruco detection
        self.goal_pose_sub = rospy.Subscriber("/goal_pose_aruco",Point ,self.goal_pose_point)

        if self._odomSubscriber == True:
            rospy.loginfo("Odom Topic going up")
        self._tolerance = tolerance
        self._odomTopic = odom_topic
        self._cmd_velTopic = cmd_vel_topic
        self.rate = rospy.Rate(10)
        self._pose = [0, 0, 0]
        self.goal_pose = [0, 0]
        self._pi = 3.141592
   
    def  goal_pose_point(self, data):
        self.goal_pose[0] = data.x
        self.goal_pose[1] = data.y
        print("Recebi a mensagem:" + str(self.goal_pose[0]))
        # self.move2goal()

    def get_position_odom(self, msg):
        self._pose[0] = msg.pose.pose.position.x
        self._pose[1] = msg.pose.pose.position.y
        rot_q = msg.pose.pose.orientation
        _, _, self._pose[2] = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

        #Function to calculate the distance between the actual and future
    def distance(self, goal_pose_, _pose):
        return sqrt(pow((goal_pose_[0]-self._pose[0]), 2) + pow((goal_pose_[1] - self._pose[1]), 2))
    
        # Function to calculate the linear vel.
    def linear_vel(self, goal_pose_, constant=1.5):
        return constant * self.distance(goal_pose_, self._pose)

        #Funcion to calculate the angle.
    def teta(self, goal_pose_, _pose):
        return atan2(goal_pose_[1] - self._pose[1], goal_pose_[0] - self._pose[0])

        # Function to move jackal
    def move2goal(self):
        vel_msg = Twist()
        print("Recebi o objetivo: " + str(self.goal_pose[0]))

       
        erroAngle = (self.teta(self.goal_pose, self._pose) - (self._pose[2]))

        if self.goal_pose [0] == [0] and self.goal_pose[1] == [0]:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
        else:

            if self.distance(self.goal_pose , self._pose) >= self._tolerance:


                # Linear velocity in the x-axis.
                if self.linear_vel(self.goal_pose) > 1:
                    vel_msg.linear.x = 0.5

                    # Angular Velocity in the z-axis.
                    vel_msg.linear.y = erroAngle
                    if(erroAngle > self._pi): 
                            erroAngle -= (2*(self._pi))
                    elif (erroAngle < -self._pi): 
                        erroAngle += (2*(self._pi))

                    vel_msg.angular.z = erroAngle

                    # Publishing our vel_msg
                    self.velocity_publisher.publish(vel_msg)
                else:
                    vel_msg.linear.x = self.linear_vel(self.goal_pose)
                    vel_msg.linear.y = 0
                    vel_msg.linear.z = 0

                    # Angular Velocity in the z-axis.
                    vel_msg.linear.y = erroAngle
                    if(erroAngle > self._pi): 
                            erroAngle -= (2*(self._pi))
                    elif (erroAngle < -self._pi): 
                        erroAngle += (2*(self._pi))

                    vel_msg.angular.z = erroAngle

                    # Publishing our vel_msg
                    self.velocity_publisher.publish(vel_msg)

            else:
                # Stopping our robot after the movement is over.
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0
                self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
            # rospy.spin()
if __name__ == "__main__":
    
    jackal = Jackal("/typea/position", "/typea/cmd_vel", 1)
    whileRate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        # jackal.test()
        jackal.move2goal()
        # rospy.spinOnce()
        whileRate.sleep()
