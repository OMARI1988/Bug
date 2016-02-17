import numpy as np
import cv2

cap = cv2.VideoCapture('/home/omari/Bugs/movies/CS3_spotted_wings.avi')
fgbg1 = cv2.BackgroundSubtractorMOG()
fgbg2 = cv2.BackgroundSubtractorMOG2(1,150,True)

while(1):
    ret, frame = cap.read()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
    image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    fgmask = fgbg2.apply(image)
    frame[fgmask>0] = (0,0,255)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
