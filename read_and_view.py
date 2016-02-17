import numpy as np
import cv2

cap = cv2.VideoCapture('/home/omari/Bugs/movies/CS1_not_tracking.avi')

# take first frame of the video
ret,frame = cap.read()

while(1):
    ret ,frame = cap.read()

    if ret == True:
        cv2.imshow('img2',frame)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite('/home/omari/Bugs/images/'+chr(k)+".png",frame)

    else:
        break

cv2.destroyAllWindows()
cap.release()
