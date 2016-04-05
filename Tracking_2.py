import numpy as np
import cv2
import colorsys
import Tkinter as tk
import Image, ImageTk
from PIL import Image, ImageTk


class Tracker(object):
    """docstring for Tracker"""
    def __init__(self):
        self._Track_flag = 1
        self._Stop_frame = 20
        self._Track_number = 0
        self._Track = {}
        self._Min = {}
        self._Time = {}
        self._Max_Track_number = 1
        self._HSV_tuples = [(x*1.0/self._Max_Track_number, 1.0, 1.0) for x in range(self._Max_Track_number)]
        self._colors = map(lambda x: colorsys.hsv_to_rgb(*x), self._HSV_tuples)

        self._cap = cv2.VideoCapture('/home/omari/Datasets_old/Zak/Calopteryx splendens/Calibration group 1/AV_Z_BD1_Seq1_020715.avi')
        self._frames = []
        while(1):
            ret, frame = self._cap.read()
            if ret:
                self._frames.append(frame)
            else:
                break
        self._N = 0
        self._N_max = len(self._frames)

        self._root = tk.Tk()
        self._w = tk.Scale(self._root, from_=0, to=self._N_max-1, length=1000, orient=tk.HORIZONTAL)
        self._w_flag = 0
        self._w.pack()
        self._w.bind("<Button-1>", self._callback2)
        self._root.bind('<Escape>', lambda e: self._root.quit())
        self._lmain = tk.Label(self._root)
        self._lmain.bind("<Button-1>", self._callback)
        self._lmain.pack()

        self._fgbg1 = cv2.BackgroundSubtractorMOG(100,10,.03,0)
        self._fgbg2 = cv2.BackgroundSubtractorMOG2(0,150,False)

    def _callback2(self,event):
        self._w_flag=1

    def _callback(self,event):
        print "clicked at", event.x, event.y
        self._Track[self._Track_number] = [[event.x,event.y]]
        self._Min[self._Track_number] = [np.inf,[]]
        self._Time[self._Track_number] = [self._Stop_frame-1]
        self._Track_number += 1
        if self._Track_number == self._Max_Track_number:
            self._Track_flag = 1

    def _show_frame(self):
        self._frame = self._frames[self._N]
        self._track_frame()
        if self._Track_flag:
            self._N += 1
        self._image = cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(self._image)
        imgtk = ImageTk.PhotoImage(image=img)
        self._lmain.imgtk = imgtk
        self._lmain.configure(image=imgtk)
        if self._N==self._Stop_frame:
            self._Track_flag = 0
        self._lmain.after(10, self._show_frame)
        if self._w_flag == 1:
            self._N = self._w.get()

    def _track_frame(self):
        gray_image = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
        image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        fgmask = self._fgbg2.apply(image)
        contours, t = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) < 1000 and cv2.contourArea(c) > 5:
                (x,y),radius = cv2.minEnclosingCircle(c)
                center = (int(x),int(y))
                radius = int(radius)
                if radius<25:
                    if 0 in self._Track:
                        for T in range(self._Max_Track_number):
                            distance = np.sqrt((self._Track[T][-1][0]-x)**2 + (self._Track[T][-1][1]-y)**2)
                            if distance < self._Min[T][0]:
                                self._Min[T][1] = [x,y]
                                self._Min[T][0] = distance
                    # cv2.circle(self._frame,center,(6),(0,0,255),2)
                    # cv2.circle(self._frame,center,(12),(0,255,0),2)
        if 0 in self._Track:
            for T in range(self._Max_Track_number):
                if self._Min[T][0] < 20:
                    self._Track[T].append(self._Min[T][1])
                    self._Time[T].append(self._N)
                self._Min[T][0] = np.inf
                self._Min[T][1] = []
                for i in range(len(self._Track[T])-1):
                    A = self._Track[T][i]
                    B = self._Track[T][i+1]
                    cv2.line(self._frame,(int(A[0]),int(A[1])),(int(B[0]),int(B[1])),(self._colors[T][0]*255,self._colors[T][1]*255,self._colors[T][2]*255),2)

def main():
    Tr = Tracker()
    Tr._show_frame()
    Tr._root.mainloop()

if __name__ == "__main__":
    main()
