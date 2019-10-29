
import sys
import numpy as np
import cv2
# Capturando o video
cap = cv2.VideoCapture(0)

# Dicionário dos arucos------------------------------------------

#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

# ---------------------------------------------------------------

while(True):
    # Pegando frame por frame
    ret, frame = cap.read()
    # Aplicando filtro de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Utilizando a função de identificar arucos
    res = cv2.aruco.detectMarkers(gray, dictionary)
    
    # Lógica para desenhar o ID e o corner principal
    if len(res[0]) > 0:
        cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#%%

