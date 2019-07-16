
import sys
#sys.path.append("/usr/local/lib/python2.7/dist-packages")
#sys.path.append("./.local/lib/python2.7/site-packages")
sys.path.append("./.local/lib/python3.5/site-packages")
import numpy as np
import cv2
#sys.path.append("/home/marco/env_marco/lib/python3.6/site-packages")
#sys.path.append("/home/marco/env_marco/lib/python3.6/site-packages")
#sys.path.append('/home/marco/anaconda3/lib/python3.6/site-packages')
cap = cv2.VideoCapture(0)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

while(True):
    ret, frame = cap.read()
    #frame = cv2.imread("/home/marco/Desktop/bags/calibrations/img2/left0003.jpg")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    res = cv2.aruco.detectMarkers(gray, dictionary)
    

    if len(res[0]) > 0:
        cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])
        if res[1][0] == 2:
            print("5")
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#%%

