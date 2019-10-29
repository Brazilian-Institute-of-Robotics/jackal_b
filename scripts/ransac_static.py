#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
import random
class ransac:
    def __init__ (self):
        self.im = cv2.imread('/home/senai/Imagens/geometry.png')
        n=0
        self.lista = []


    def filters (self):
        #Método para transformar a imagem em greyscale
        self.gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        #Para separar o que é preto de branco:
        ret, self.thresh = cv2.threshold(self.gray, 118, 255, cv2.THRESH_BINARY)
        self.th3 = cv2.adaptiveThreshold(self.gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        #Métodos para achar contornos
        self.edges = cv2.Canny(self.thresh,0,200)
    def coords_saving (self):
        #The numpy.where() method to retrieve a tuple indices of two arrays where the first array contains the x-coordinates of the white points and the second array contains the y-coordinates of the white pixels.
        indices = np.where(self.edges != [0])
        #Organizando em uma tupla
        coordinates = zip(indices[0], indices[1])
        #Pegando posições randomicas
        random_coords =random.choice(coordinates)
        #print(random_coords)
        three_points = self.lista
        if len(three_points) < 3:
            three_points.append(random_coords)

        if len(three_points) == 3: 
            x_1 =three_points[0][0]
            x_2 = three_points[1][0]
            xm = (x_1+x_2)/2
            y_1 = three_points[0][1]
            y_2 = three_points[1][1]
            ym = (y_1+y_2)/2
            pm = (xm+ym)/2
            print((ym))
            print(xm)
            print(pm)
            




        
        #dist = np.linalg.norm(random_coords[0]-random_coords[1])
        #print (dist)
        n = 3791

        #for n in coordinates:
        #    print (max(coordinates))

    def imgshow(self):
        #while (True):

        cv2.imshow('frame',self.edges)
        #Para cancelar o programa com ctrl c
        if cv2.waitKey(1) & 0xFF == ord('q'):
            None


if __name__ == "__main__":
    rec = ransac()

    while True:
        rec.filters()
        rec.imgshow()
        rec.coords_saving()



    #%%

