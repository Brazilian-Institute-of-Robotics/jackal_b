#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2


#Função para capturar a imagem da webcam
cap = cv2.VideoCapture(0) 

while(True):
    #Pegando cada frame proveniente da imagem da webcam
    _, frame = cap.read()

    #Invertendo RGB para BGR
    imagem = cv2.bitwise_not(frame)
    kernel = np.ones((5,5),np.uint8)

    # Convertendo BGR para HSV
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV) 

    # Definindo o range da cor vermelha em HSV
    lower_red = np.array([80,70,50]) #Menor valor
    upper_red = np.array([90,255,255]) #Maior valor

    #Identificação e segmentação de edges
    edges = cv2.Canny(frame,100,200)

    # Threshold de HSV para apenas pegar vermelho
    mask = cv2.inRange(hsv, lower_red, upper_red)

    #Utilização de tratamento de imagem - Opening
    opening =cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    opening2 = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

    #Utilização de tratamento de imagem - Closing
    closing = cv2.morphologyEx(opening2, cv2.MORPH_CLOSE, kernel)

    # Retornando imagem com pixels que não são zero
    res = cv2.bitwise_and(frame,frame, mask= closing)
    
    # Mostrando a imagem em uma janela
    cv2.imshow('edges',edges) 
    # Mostrando a imagem em uma janela
    cv2.imshow('frame',frame)
    # Mostrando a imagem em uma janela
    cv2.imshow('mask', mask)
    # Mostrando a imagem em uma janela
    cv2.imshow('res',res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Quando tudo estiver finalizado, libere a captura de imagem
cap.release()
cv2.destroyAllWindows()
