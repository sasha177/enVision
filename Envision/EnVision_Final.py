import cv2
import numpy as np
import time

#The following code uses user input and print statements to introduce the program to the user!

name = input("Enter your name: ")
print("Hello", name + "!")
time.sleep(2)
print("Thank you for using Envision. Lets get started with a quick diagnostic!")
time.sleep(3)
print("The following program will now measure your blinking rate. Let's get started!")
time.sleep(3)


def timer(minutes):
    seconds = minutes * 60
    start = time.time()
    time.clock()
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
    time.sleep(1)
    print ('also printing Done so you can see it')


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
c=0
cap = cv2.VideoCapture(0)
jets = 60
t_end = time.time() + jets * 1
#time.time() < t_end

#This loop measures the user's blink rate for one minute and reports it back
while time.time() < t_end:
    ret,img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        k=1
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            k=0
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)
        if k==1:
            print("You've blinked ", c, " times")
            c=c+1
        else:
            print("Not blinking!")
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()
cv2.destroyAllWindows()

#reassigns the user blinking rate as the threshold value
threshold = c

print("According to the diagnostic, your blinking rate is ", str(threshold) + " blinks per", str(jets) + "seconds!")

t_end = time.time() + 60 * 1
c=0
cap = cv2.VideoCapture(0)
time.sleep(5)

#starts the constant scanning of the user's blinking and lets the user know if they need to take a break because they didn't meet the threshold
while True:
    while time.time() <= t_end:
        ret,img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            k=1
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                k=0
                cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)
            if k==1:
                print("You've blinked ",c," times")
                c=c+1
            #else:
                #print(" ")
        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if time.time() >= t_end:
            if c < threshold:
                print("It looks like your eyes could use some rest. Envision recommend taking a break and doing some eye exercises!")
                c=0
                t_end = time.time() + 60 * 1
            else:
                print("You met the threshold!") #the actual product would not notify the user if they meet the threshold, but this is done here in the prototype to show the proof of concept
                c=0
                t_end = time.time() + 60 * 1
        if k==27:
            break
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()