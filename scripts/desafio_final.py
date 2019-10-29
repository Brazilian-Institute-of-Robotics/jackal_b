#!/usr/bin/env python

import rospy
import sys
import cv2
import numpy as np
from std_msgs.msg import Float64
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dynamixel_msgs.msg import JointState

# A classe Motor_movement tem como intuito o controle dos dynamixels
class motor_movement():

    def __init__(self):

        # Subscribers nos tópicos dos motores (joint1 e joint2)
        self.joint1_sub = rospy.Subscriber("/joint1_controller/state", JointState, self.joint1_callback)
        self.joint2_sub = rospy.Subscriber("/joint2_controller/state", JointState, self.joint2_callback)

        # Publicar nos tópicos dos motores para que eles se movimentem
        self.joint1_pub = rospy.Publisher("/joint1_controller/command", Float64, queue_size=10)          # joint1
        self.joint2_pub = rospy.Publisher("/joint2_controller/command", Float64, queue_size=10)         #  joint2

        # Váriaves
        self.joint1_position = 0
        self.joint2_position = 0

    # Função de callback para saber a posição do dynamixel joint 1.
    def joint1_callback(self, msg):
        self.joint1_position = msg.current_pos
    
    # Função de callback para saber a posição do dynamixel joint 2.
    def joint2_callback(self, msg):
        self.joint2_position = msg.current_pos
        
    # Função para publicar a posição desejada.       
    def pub_movement(self, joint1, joint2):
        self.joint1_pub.publish(joint1)
        self.joint2_pub.publish(joint2)


# A classe Image é para a identificação do Aruco.
class image():
   
    def __init__(self):
        # Vamos trabalhar com arucos da família original.
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        # Pegando a imagem da câmera
        self.cap = cv2.VideoCapture(0)

    def capture(self):
        # Estanciando a classe anterior a váriavel m_v
        self.m_v = motor_movement()
        
        # Váriavel da imagem
        __, frame = self.cap.read()
        print(frame)
        # Convertando em escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Aplicando o dicionário
        res = cv2.aruco.detectMarkers(gray, self.dictionary)
        # Lógica de identificação dos arucos
        if len(res[0]) > 0:
            cv2.aruco.drawDetectedMarkers(frame,res[0],res[1])
            #Lógica para mandar a informação de posição para o motor
            if res[1][0] == 8:
                self.m_v.pub_movement(0, 4000)
            else: 
                self.m_v.pub_movement(4000, 0)
        

        #cv2.namedWindow('cv_image', cv2.WINDOW_NORMAL)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            quit()


def main():
    im = image()
    # Começando o nó para os motores funcionarem
    rospy.init_node("joints", anonymous=True)
    # Frequência
    rate = rospy.Rate(60)
    
    while(not rospy.is_shutdown()):
        im.capture()
        rate.sleep()

if __name__ == "__main__":
    main()