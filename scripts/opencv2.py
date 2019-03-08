#!/usr/bin/env python
from __future__ import print_function
import sys
#sys.path.append("/usr/local/lib/python2.7/dist-packages")
#sys.path.append("./.local/lib/python2.7/site-packages")
sys.path.append("./.local/lib/python3.5/site-packages")
import roslib
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Point


#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)


class image_converter:


  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image,  queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/rrbot/camera1/image_raw",Image,self.callback)
    # Place to goal
    self.goal_pose_pub = rospy.Publisher("/goal_pose_aruco", Point, queue_size=10)
   
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)
    # Variable of image
    frame = cv_image
    # Converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Using the dictionary of arucos
    res = cv2.aruco.detectMarkers(gray, dictionary)
    
    if len(res[0]) > 0:
        cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])
        #logic to reconize
        if res[1][0] == 1:
            goal = Point()
            goal.x = 6
            goal.y = 4
            self.goal_pose_pub.publish(goal)
     
    cv2.namedWindow('cv_image', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',cv_image)
    
    cv2.waitKey(3)
    
    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)