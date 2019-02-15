#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from math import pow, atan2, sqrt
from tf.transformations import euler_from_quaternion

class Jackal():

    def __init__(self, odom_topic, cmd_vel_topic,tolerance):
        # Creates a node with name 'jackal' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('jackal', anonymous=True)

        # Publisher which will publish to the topic '/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/cmd_vel',
                                                  Twist, queue_size=10)

        #location with odometry
        self._odomSubscriber = rospy.Subscriber("/odometry/filtered", 
                                                Odometry, self.get_position_odom)
        if self._odomSubscriber == True:
            rospy.loginfo("Odom Topic going up")
        self._tolerance = tolerance
        self._odomTopic = odom_topic
        self._cmd_velTopic = cmd_vel_topic
        self.rate = rospy.Rate(10)
        self._pose = [0, 0, 0]
        self.goal_pose = [0, 0]
        self._pi = 3.141592
       
        
        #inputs
        self.goal_pose[0] = input("Set your x goal: ")
        self.goal_pose[1] = input("Set your y goal: ")
        
    
    def get_position_odom(self, msg):
        self._pose[0] = msg.pose.pose.position.x
        self._pose[1] = msg.pose.pose.position.y
        rot_q = msg.pose.pose.orientation
        _, _, self._pose[2] = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

        #metodo de distancia entre a atual e a futura
    def distance(self, goal_pose, _pose):
        return sqrt(pow((self.goal_pose[0]-self._pose[0]), 2) + pow((self.goal_pose[1] - self._pose[1]), 2))
        print("oi")
        
        # Function to move the robot
    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.distance(self.goal_pose, self._pose)
    
   # def steering_angle(self, goal_pose):
    #    return atan2(self.goal_pose[1] - self._pose[1], self.goal_pose[0] - self._pose[0])

    #def angular_vel(self, goal_pose, constant=6):
     #   return constant * (self.steering_angle(self.goal_pose))
    
    def move2goal(self):
        vel_msg = Twist()

        teta = atan2(self.goal_pose[1] - self._pose[1], self.goal_pose[0] - self._pose[0])
        erroAngle = (teta - (self._pose[2]))

        if self.distance(self.goal_pose , self._pose) >= self._tolerance:
            

            # Linear velocity in the x-axis.
            if self.linear_vel(self.goal_pose) > 1:
                vel_msg.linear.x = 0.5
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
            rospy.spin()
if __name__ == "__main__":
    
    jackal = Jackal("/typea/position", "/typea/cmd_vel", 1)
    whileRate = rospy.Rate(10)
    
    while(not rospy.is_shutdown()):
        jackal.move2goal()
        whileRate.sleep()
