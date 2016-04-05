from Tkinter import *
import cv2
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join

class App():
    """docstring for App"""
    def __init__(self, master):
        # variables
        self.master = master
        # self.save_sk_img = 1
        #
        # self.video_iter = 0
        # self.all_videos = [v for v in listdir(directory)]
        # self.video = self.all_videos[self.video_iter]
        #
        # self.video_len = 0
        # self.start = -1
        # self.stop = -1
        # # self.directory = directory
        # # self.dir = join(self.directory, self.video)


        row = 0
        # activity
        bug_type = ("Choose ..", "Calopteryx splendens", "Ischnura elegans", "Libellula quadrimaculata", "Orthetrum cancellatum", "Sympetrum striolatum")
        Label(master, text="species").grid(row=row, pady=10, sticky=W+E)
        self.variable = StringVar(master)
        self.variable.set(bug_type[0]) # default value
        self.menu_species = OptionMenu(master, self.variable, *bug_type)
        self.menu_species.grid(row=row, column=1, stick="ew")
        self.menu_species.configure(bg = "WHITE")  # Set background color to WHITE
        self.menu_species.configure(activebackground = "LIGHTBLUE")  # Set activebackground color to LIGHTBLUE
        row+=1

        # region
        collections = ("","")
        Label(master, text="collections").grid(row=row, pady=10, sticky=W+E)
        self.variable_r = StringVar(master)
        self.variable_r.set(collections[0]) # default value
        self.menu_folder = OptionMenu(master, self.variable_r, *collections)
        self.menu_folder.grid(row=row, column=1, stick="ew")
        self.menu_folder.configure(bg = "WHITE")  # Set background color to green
        self.menu_folder.configure(activebackground = "LIGHTBLUE")  # Set background color to green
        row+=1

        # start stop
        Button(master, text="start", command=self.button_start_callback).grid(row=row, pady=3, sticky=W+E)
        self.L_start = StringVar()
        Label(master, textvariable=self.L_start).grid(row=row,column=1, pady=3, sticky=W+E)
        row+=1
        Button(master, text="stop", command=self.button_stop_callback).grid(row=row,  pady=3, sticky=W+E)
        self.L_stop = StringVar()
        Label(master, textvariable=self.L_stop).grid(row=row,column=1, pady=3, sticky=W+E)
        row+=1

        # next and previous frames
        Button(master, text="Next frame", command=self.next_f_callback).grid(row=row, column=0, pady=3, sticky=W+E)
        Button(master, text="Prev frame", command=self.prev_f_callback).grid(row=row, column=1, pady=3, sticky=W+E)
        row+=1

        # next and previous videos
        Button(master, text="Next video", command=self.next_callback).grid(row=row, column=0, pady=3, sticky=W+E)
        Button(master, text="Prev video", command=self.prev_callback).grid(row=row, column=1, pady=3, sticky=W+E)
        row+=1

        # add label button
        Button(master, text="Add action", command=self.add_callback).grid(row=row, column=0, pady=10, sticky=W+E, columnspan=2)
        row+=1

        # empty labels
        self.L_empty = Label(master).grid(row=row,column=0, pady=100, padx=60, sticky=W+E)
        self.L_empty = Label(master).grid(row=row,column=1, pady=100, padx=120, sticky=W+E)
        row+=1
        # self.row = row
        #
        # # images
        # self.image = Label()
        # self.image.grid(row=0, rowspan=row, column=2)
        # self.load_video()
        #
        # # slider
        # self.scale_l = Scale(master, from_=1, to=self.video_len, orient=HORIZONTAL, command=self.scale_callback)
        # self.scale_l.grid(row=row, column=2, pady=5, sticky=W+E)
        # self.row = row

    def add_callback(self):
        if self.new_vid:
            r = self.variable_r.get()
            self.file_meta.write('region_id:'+str(self.RegionIDs[r])+'\n')
            self.file_meta.write('region:'+r+'\n')
            self.new_vid = 0
        act = ''
        if int(self.start)>0 and int(self.stop)>0:
            if int(self.start) < int(self.stop):
                act += 'label:'
                act += self.variable.get()+':'+self.start+','+self.stop
                self.file.write(act+'\n')
        print '  -adding: ',act

    def next_f_callback(self):
        self.scale_l.set(int(self.scale_l.get())+1)

    def prev_f_callback(self):
        self.scale_l.set(int(self.scale_l.get())-1)

    def next_callback(self):
        if self.video_iter+1 < len(self.all_videos):
            self.video_iter += 1
            self.video = self.all_videos[self.video_iter]
            self.dir = join(self.directory, self.video)
            self.load_video()
            self.update_image('00001')
        else:
            print "All videos annotated in %s" % self.directory
            complete_labelling = open(self.directory + '/completed_labelling.txt', 'a')
            pass

    def prev_callback(self):
        self.video_iter -= 1
        if self.video_iter < 0: self.video_iter = 0

        self.video = self.all_videos[self.video_iter]
        self.dir = join(self.directory, self.video)
        self.load_video()
        self.update_image('00001')

    def load_video(self):
        self.new_vid = 1
        print "loading next video:", self.video
        self.video_len = len([f for f in listdir(join(self.dir, "skeleton")) if isfile(join(self.dir, "skeleton", f))])
        self.scale_l = Scale(self.master, from_=1, to=self.video_len, orient=HORIZONTAL, command=self.scale_callback)
        self.scale_l.grid(row=self.row , column=2, pady=5, sticky=W+E)
        self.start = -1
        self.stop = -1
        self.file = open(self.dir+'/labels.txt','a')
        self.file_meta = open(self.dir+'/meta.txt','w')

    def button_start_callback(self):
        self.L_start.set(str(int(self.scale_l.get())))
        self.start = str(int(self.scale_l.get()))

    def button_stop_callback(self):
        self.L_stop.set(str(int(self.scale_l.get())))
        self.stop = str(int(self.scale_l.get()))

    def scale_callback(self, val):
        if int(val)<10:         val_str = '0000'+str(val)
        elif int(val)<100:      val_str = '000'+str(val)
        elif int(val)<1000:     val_str = '00'+str(val)
        elif int(val)<10000:    val_str = '0'+str(val)
        elif int(val)<100000:   val_str = str(val)
        self.update_image(val_str)

    def update_image(self,val_str):
        img_loc = join(self.dir, "rgb", "rgb_"+val_str+'.jpg')
        img = cv2.imread(img_loc)
        img = self.plot_sk(img,val_str)
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(self.img)
        photo = ImageTk.PhotoImage(img)
        self.image = Label(image=photo)
        self.image.image = photo # keep a reference!
        self.image.grid(row=0, padx=2, rowspan=self.row , column=2, sticky=E)

    def plot_sk(self,img,val_str):
        self.get_2d_sk(val_str)
        img = self.plot_2d_sk(img)

        if self.save_sk_img:
            cv2.imwrite(join(self.dir, "rgb_sk", "sk_"+val_str+'.jpg'),img)
        return img

    def get_2d_sk(self,val_str):
        fx = 525.0
        fy = 525.0
        cx = 319.5
        cy = 239.5
        f1 = open(join(self.dir,'skeleton','skl_'+val_str+'.txt'),'r')
        for count,line in enumerate(f1):
            # read the joint name
            if (count-1)%10 == 0:
                j = line.split('\n')[0]
                self.skeleton_data[j] = [0,0,0,0,0]
            # read the x value
            elif (count-1)%10 == 2:
                a = float(line.split('\n')[0].split(':')[1])
                self.skeleton_data[j][0] = a
            # read the y value
            elif (count-1)%10 == 3:
                a = float(line.split('\n')[0].split(':')[1])
                self.skeleton_data[j][1] = a
            # read the z value
            elif (count-1)%10 == 4:
                a = float(line.split('\n')[0].split(':')[1])
                self.skeleton_data[j][2] = a
                #2D data
                x = self.skeleton_data[j][0]
                y = self.skeleton_data[j][1]
                z = self.skeleton_data[j][2]
                x2d = int(x*fx/z*1 +cx);
                y2d = int(y*fy/z*-1+cy);
                self.skeleton_data[j][3] = x2d
                self.skeleton_data[j][4] = y2d

    def plot_2d_sk(self,img):
        for j in self.connected_joints:
            x0 = self.skeleton_data[j[0]][3]
            y0 = self.skeleton_data[j[0]][4]
            x1 = self.skeleton_data[j[1]][3]
            y1 = self.skeleton_data[j[1]][4]
            # print j[0],x0,y0,j[1],x1,y1
            cv2.line(img,(x0,y0),(x1,y1),(240,0,180), 3)

        for j in self.joints:
            x = self.skeleton_data[j][3]
            y = self.skeleton_data[j][4]
            cv2.circle(img,(x,y),5, (240,0,50), -1)
            if j == 'head':
                cv2.circle(img,(x,y),9, (255,0,50), -1)
            if j == 'right_hand':
                cv2.circle(img,(x,y),5, (0,255,50), -1)
        return img


directory = '/home/omari/Datasets_old/Lucie/'
date_files = [f for f in listdir(directory)]
files_remaining = [f for f in date_files if not isfile(join(directory, f, "completed_labelling.txt"))]
print files_remaining

def main():
    root = Tk()
    App(root)
    root.mainloop()

if __name__=="__main__":
    main()
