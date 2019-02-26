
import sys
#sys.path.append("/usr/local/lib/python2.7/dist-packages")
#sys.path.append("./.local/lib/python2.7/site-packages")
sys.path.append("./.local/lib/python3.5/site-packages")
import numpy as np
import cv2
import sys
cap = cv2.VideoCapture(0)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

while(True):
    _, frame = cap.read()
    #invert bgr
    imagem = cv2.bitwise_not(frame)
    
    kernel = np.ones((5,5),np.uint8)
    # Convert the BGR to HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV) 
    # Define the range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    lower_red = np.array([80,70,50])
    upper_red = np.array([90,255,255])

    #edges
    edges = cv2.Canny(frame,100,200)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #opening
    opening =cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    opening2 = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
    #closing
    closing = cv2.morphologyEx(opening2, cv2.MORPH_CLOSE, kernel)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= closing)
    cv2.imshow('edges',edges)
    cv2.imshow('frame',frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res',res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
