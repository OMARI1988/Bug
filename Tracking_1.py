import numpy as np
import cv2
import colorsys

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


global Track_flag,Track_number
Track_flag = 1
Stop_frame = 10
Track_number = 0
Max_Track_number = 8
HSV_tuples = [(x*1.0/Max_Track_number, 1.0, 1.0) for x in range(Max_Track_number)]
colors = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

def get_track(event,x,y,flags,param):
    global Track_flag,Track_number,Max_Track_number,Stop_frame
    if event == cv2.EVENT_LBUTTONDBLCLK:
        Track[Track_number] = [[x,y]]
        Min[Track_number] = [np.inf,[]]
        Time[Track_number] = [Stop_frame-1]
        Track_number += 1
        if Track_number == Max_Track_number:
            Track_flag = 0

cap = cv2.VideoCapture('/home/omari/Bugs/movies/CS1_not_tracking.avi')
fgbg1 = cv2.BackgroundSubtractorMOG(100,10,.03,0)
fgbg2 = cv2.BackgroundSubtractorMOG2(0,150,False)

cv2.namedWindow('video')
cv2.setMouseCallback('video',get_track)

frames = []
Track = {}
Time = {}
Min = {}
while(1):
    ret, frame = cap.read()
    if ret:
        frames.append(frame)
    else:
        break

for count,frame in enumerate(frames):
    print 'processing frame number : ',count+1
    if count==Stop_frame:
        while(Track_flag):
            k = cv2.waitKey(30) & 0xff
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
                if 0 in Track:
                    for T in range(Max_Track_number):
                        distance = np.sqrt((Track[T][-1][0]-x)**2 + (Track[T][-1][1]-y)**2)
                        if distance < Min[T][0]:
                            Min[T][1] = [x,y]
                            Min[T][0] = distance
                # cv2.circle(frame,center,(6),(0,0,255),2)
                # cv2.circle(frame,center,(12),(0,255,0),2)

    if 0 in Track:
        for T in range(Max_Track_number):
            if Min[T][0] < 20:
                Track[T].append(Min[T][1])
                Time[T].append(count)
            Min[T][0] = np.inf
            Min[T][1] = []
            for i in range(len(Track[T])-1):
                A = Track[T][i]
                B = Track[T][i+1]
                cv2.line(frame,(int(A[0]),int(A[1])),(int(B[0]),int(B[1])),(colors[T][0]*255,colors[T][1]*255,colors[T][2]*255),2)
            # X = []
            # Y = []
            # for i in range(len(Track[T])):
            #     X.append(Track[T][i][0])
            #     Y.append(Track[T][i][1])
            # if len(X)>4:
            #     polynomial_features = PolynomialFeatures(degree=10,
            #                                  include_bias=False)
            #     linear_regression = LinearRegression()
            #     pipeline = Pipeline([("polynomial_features", polynomial_features),
            #                          ("linear_regression", linear_regression)])
            #     time = np.sort(Time[T])
            #     pipeline.fit(time[:, np.newaxis], X)
            #     X = pipeline.predict(time[:, np.newaxis])
            #     pipeline.fit(time[:, np.newaxis], Y)
            #     Y = pipeline.predict(time[:, np.newaxis])
            #     for i in range(len(X)-1):
            #         t1 = Time[T][i]
            #         t2 = Time[T][i+1]
            #         cv2.line(frame,(int(X[i]),int(Y[i])),(int(X[i+1]) , int(Y[i+1])),(colors[T][0]*255,colors[T][1]*255,colors[T][2]*255),2)


    cv2.imshow('video',frame)
    if count<10:
        frame_name = '000'+str(count)+'.jpg'
    elif count<100:
        frame_name = '00'+str(count)+'.jpg'
    elif count<1000:
        frame_name = '0'+str(count)+'.jpg'
    cv2.imwrite('/home/omari/Bugs/images/frame_'+frame_name,frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
