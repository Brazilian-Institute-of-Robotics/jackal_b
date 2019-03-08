import numpy as np
import cv2
import cv2.aruco as aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

id = 250
img = aruco.drawMarker(aruco_dict, id, 700)
cv2.imwrite("marker_%d.jpg"%id, img)
 
cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
