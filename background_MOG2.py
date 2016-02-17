import numpy as np
import cv2

cap = cv2.VideoCapture('/home/omari/Bugs/movies/CS3_spotted_wings.avi')

fgbg2 = cv2.BackgroundSubtractorMOG2()
fgbg1 = cv2.BackgroundSubtractorMOG()

# img = np.zeros((1024,2048),dtype=np.uint8)

while(1):
    ret, frame = cap.read()
    if ret:
        fgmask1 = fgbg1.apply(frame)
        fgmask2 = fgbg2.apply(frame)
        # img[:,0:1024] = fgmask1
        # img[:,1024:] = fgmask2
        frame[fgmask2==255] = (0,0,255)

        cv2.imshow('frame',frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
