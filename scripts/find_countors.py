#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys

#cap = cv2.VideoCapture(0)

while True:
    #Método para capturar a imagem da câmera
    #__, frame = cap.read()
    #Método para carregar a imagem
    im = cv2.imread('/home/senai/Imagens/geometry.png')
    #Método para transformar a imagem
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #Para separar o que é preto de branco:
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    #Métodos para achar contornos
    edges = cv2.Canny(im,100,200)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #To draw all the contours in an image
    #img = cv2.drawContours(im, contours, -1, (0,255,0), 3)
    #To draw an individual contour:
    #img = cv2.drawContours(im, contours, 3, (0,255,0), 3)
    #Best method to draw countours
    cnt = contours[0]
    img = cv2.drawContours(im, [cnt], 0, (0,255,0), 3)
    #cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    #Contour area
    area = cv2.contourArea(cnt)
    if area == 5852:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'This is a square!',(10,550), font, 1, (255,255,255), 2, cv2.LINE_AA)

    #Mostrar a imagem
    cv2.imshow('edges',edges)
    cv2.imshow('frame',im)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()