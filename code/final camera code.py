import numpy
from numpy import matrix
from numpy import array
from cv2 import *
import cv2

from cStringIO import StringIO
import RPi.GPIO as GPIO
import pygame
import time
GPIO.setmode(GPIO.BCM)

VAL1 = 23
VAL2 = 24
VAL3 = 25
VAL4 = 8
GPIO.setup(VAL1,GPIO.IN)
GPIO.setup(VAL2,GPIO.IN)
GPIO.setup(VAL3,GPIO.IN)
GPIO.setup(VAL4,GPIO.IN)
pygame.mixer.init()

cap = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)
###scaling the feed by 2.5
cap.set(3,320)
cap.set(4,240)
cap2.set(3,320)
cap2.set(4,240)

mtx1 = matrix ([[764.98, 0, 289.39] , [ 0.00 , 737.15, 126.47] , [0, 0, 1]])
dist1 = array([[-0.45602], [1.2886], [0.01138], [-0.00035], [-2.2178]])
ncm1 = matrix ([[587.96, 0.0 , 290.09],[0.00, 593.05, 112.86],[0.00, 0.00, 1.00]])

mtx2 = matrix ([[751.81, 0.00, 273.05],[0.00, 734.09, 182.54],[0,0,1]])
dist2 = array([[-0.29078] , [0.93268], [-0.00358], [-0.00244], [-2.3101]])
ncm2 = matrix ([[608.69, 0.00, 242.99],[0.00, 651.44, 178.13],[0, 0, 1]])

window_size = 15
min_disp =0
num_disp = 64
stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        preFilterCap = 12,
        blockSize = 3,
        P1 = 3000,
        P2 = 3600,
        disp12MaxDiff = 1,
        uniquenessRatio = 2,
        speckleWindowSize = 100,
        speckleRange = 1,
        mode = False
)

countu=0
countul2=0
countur2=0
stop=0
kernel = numpy.ones((2,2),numpy.uint8)
kernel2 = numpy.ones((5,5),numpy.uint8)
kernel3= numpy.ones((5,5),numpy.uint8)
while(True):
     r = GPIO.input(VAL1)
     l = GPIO.input(VAL2)
     r2 = GPIO.input(VAL3)
     l2 = GPIO.input(VAL4)
     # Capture frame-by-frame
     ret, frame = cap.read()
     ret2,frame2 = cap2.read()
     
     count=0
     countl2=0
     countr2=0
     countl1=0
     countr1=0
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
     
     
     disp = stereo.compute(gray,gray2).astype(numpy.float32) / 16.0
     disp = (disp-min_disp)/num_disp

     
     th = cv2.threshold(disp , 0.5, 0.8, cv2.THRESH_BINARY)[1]
     morphology = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel2)
     morph = cv2.morphologyEx(morphology, cv2.MORPH_OPEN, kernel2)

     morph2=cv2.erode(morph,kernel3,iterations=1)
     
     for x in range(133,186):
          for y in range (59,197):
               if morph2[y,x]>0.2:
                    count=count+1
     if count>20:
          for x in range(87,140):
               for y in range (49,197): 
                    if morph2[y,x]>0.2:
                         countl1=countl1+1
          if countl1>20:
              for x in range(180,233):
                   for y in range (49,197): 
                        if morph2[y,x]>0.2:
                             countr1=countr1+1
              if countr1>20:
                  for x in range(40,93):
                      for y in range (59,197):
                            if morph2[y,x]>0.2:
                                 countl2=countl2+1
              if countl2>20:
                  for x in range(226,279):
                       for y in range (59,197): 
                            if morph2[y,x]>0.2:
                                 countr2=countr2+1
     if count <20 and (l==0 and r==0):
          countu=countu+1
          countul2=0
          countur2=0
          stop=0
     elif (countl2 <20 or countl1<20)and l==0 and l2==0:
          countul2=countul2+1
          countu=0
          countur2=0
          stop=0
     elif (countr2 <20 or countr1<20) and r==0 and r2==0:
         countur2=countur2+1
         countu=0
         countul2=0
         stop=0
     else:
          stop=stop+1
          countu=0
          countul2=0
          countur2=0

     if countu>6:
        countu=0
        pygame.mixer.music.load("proceedforward.wav")
        pygame.mixer.music.play()
     elif countul2>6:
        countul2=0
        pygame.mixer.music.load("stepleft.wav")
        pygame.mixer.music.play()
     elif countur2>6:
        countu2=0
        pygame.mixer.music.load("stepright.wav")
        pygame.mixer.music.play()
     elif stop>6:
        stop=0
        pygame.mixer.music.load("turnaround.wav")
        pygame.mixer.music.play()
     cv2.imshow('disparity',disp)
     cv2.imshow('Thresh 0.6',th)
     cv2.imshow('Morphed', morph2)
     cv2.imshow('frame',frame)
     cv2.imshow('frame2',frame2)
     if cv2.waitKey(1) & 0xFF == ord('q'):
         break
 
 # When everything done, release the capture
cap.release()
cap2.release()
cv2.destroyAllWindows()
