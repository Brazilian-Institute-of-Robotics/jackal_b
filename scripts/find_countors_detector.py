#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys

class detector:
    def __init__ (self):
        self.im = cv2.imread('/home/senai/Imagens/geometry.png')

    def filters (self):
        #Método para transformar a imagem
        self.imgray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        #Para separar o que é preto de branco:
        ret, self.thresh = cv2.threshold(self.imgray, 127, 255, 0)
        #Métodos para achar contornos
        self.edges = cv2.Canny(self.im,100,200)
        #Method to find contours
        image, contours, hierarchy = cv2.findContours(self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #Best method to draw countours
        i = 0
        for i in 10:
            cnt = contours[i]
            img = cv2.drawContours(self.im, [cnt], 0, (0,255,0), 3)
    def imgshow(self):
        while True:
            cv2.imshow('edges',self.edges)
            cv2.imshow('frame',self.im)
            #Para cancelar o programa com ctrl c
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
if __name__ == "__main__":
    dec = detector()

    while True:
        dec.filters()
        dec.imgshow()


    #%%


cv2.waitKey(0)
cv2.destroyAllWindows()