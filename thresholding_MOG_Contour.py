import numpy as np
import cv2

cap = cv2.VideoCapture('/home/omari/Bugs/movies/CS1_not_tracking.avi')
fgbg1 = cv2.BackgroundSubtractorMOG(100,10,.03,0)
fgbg2 = cv2.BackgroundSubtractorMOG2(0,150,False)

frames = []
while(1):
    ret, frame = cap.read()
    if ret:
        frames.append(frame)
    else:
        break

for count,frame in enumerate(frames):
    print count
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
    image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    fgmask = fgbg2.apply(image)

    contours, t = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 1000 and cv2.contourArea(c) > 5:
            (x,y),radius = cv2.minEnclosingCircle(c)
            center = (int(x),int(y))
            radius = int(radius)
            if radius<25:
                cv2.circle(frame,center,(6),(0,0,255),2)
                cv2.circle(frame,center,(12),(0,255,0),2)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
