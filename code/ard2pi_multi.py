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
#GPIO.setup(VAL3,GPIO.IN)
#GPIO.setup(VAL4,GPIO.IN)
pygame.mixer.init()
while True:
    x = GPIO.input(VAL1)
    y = GPIO.input(VAL2)
    #z = GPIO.input(VAL3)
    #a = GPIO.input(VAL4)
    if x == 0 and y == 0:
        print "Proceed Forward"
        pygame.mixer.music.load("proceedforward.wav")
        pygame.mixer.music.play()
        time.sleep(3)

    elif x == 1 and y == 0:
        print "Step Right"
        pygame.mixer.music.load("stepright.wav")
        pygame.mixer.music.play()
        time.sleep(3)
    elif x == 0 and y == 1:
        print "Step Left"
        pygame.mixer.music.load("stepleft.wav")
        pygame.mixer.music.play()
        time.sleep(3)

    else:
        print "Problem ahead"
        pygame.mixer.music.load("turnaround.wav")
        pygame.mixer.music.play()
        time.sleep(3)
    #if x == 1 & y == 1:
     #   if z == 0 & a == 0:
      #      print "Step Left"
       # if z == 0 & a == 1:
        #    print "Step Left"
        #if z == 1 & a == 0:
         #   print "Step Right"
        #if z == 1 & a == 1:
         #   print "No path ahead, turn around"
    #print "Sensor 1",x
    #print "Sensor 2",y
    #if GPIO.input(VAL1)==0:
    #elif GPIO.input(VAL1)==1:
    #    print "Sensor 1",1
    #if GPIO.input(VAL2)==0:
    #elif GPIO.input(VAL2)==1:
     #   print "Sensor 2",1
    #if GPIO.input(VAL3)==0:
     #   print "Sensor 3",0
    #elif GPIO.input(VAL3)==1:
     #   print "Sensor 3",1
    #if GPIO.input(VAL4)==0:
     #   print "Sensor 4",0
    #elif GPIO.input(VAL4)==1:
     #   print "Sensor 4",1
        
GPIO.cleanup()
