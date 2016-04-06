from Tkinter import *
import cv2
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join
import Tkconstants, tkFileDialog

class App():
    """docstring for App"""
    def __init__(self, master):
        # variables
        self.master = master
        self.dir_opt = {}

        # GUI
        self.row = 0
        # browse folder
        Label(master, text="video").grid(row=self.row, column=0, pady=10, padx=2, sticky=W+E)
        self.label_browse = Label(master, text="please select a video")
        self.label_browse.grid(row=self.row, column=1, columnspan=2, pady=10, padx=2, sticky=W+E)
        self.button_dir = Button(master, text='add video', command=self.askdirectory)
        self.button_dir.grid(row=self.row, column=3, pady=10, padx=2, sticky=W+E)
        self.button_dir.configure(activebackground = "LIGHTBLUE")  # Set activebackground color to LIGHTBLUE
        self.row+=1

        # bug type
        bug_type = ("Choose ..", "Calopteryx splendens", "Ischnura elegans", "Libellula quadrimaculata", "Orthetrum cancellatum", "Sympetrum striolatum")
        Label(master, text="species").grid(row=self.row, pady=10, padx=2, sticky=W+E)
        self.variable = StringVar(master)
        self.variable.set(bug_type[0]) # default value
        self.menu_species = OptionMenu(master, self.variable, *bug_type)
        self.menu_species.grid(row=self.row, padx=2, column=1, columnspan=2, stick="ew")
        self.menu_species.configure(bg = "WHITE")  # Set background color to WHITE
        self.menu_species.configure(activebackground = "LIGHTBLUE")  # Set activebackground color to LIGHTBLUE
        self.button_load = Button(master, text="Load", command=self.button_load_callback)
        self.button_load.grid(row=self.row, padx=2, column=3, sticky=W+E)
        self.button_load.configure(activebackground = "LIGHTBLUE")  # Set activebackground color to LIGHTBLUE
        self.row+=1

        # separator
        # self.L_empty = Label(master).grid(row=self.row,column=0, pady=1, padx=60, sticky=W+E)
        # self.row+=1
        separator = Frame(height=5, bd=1, relief=SUNKEN)
        separator.grid(row=self.row, columnspan=4, sticky="ew")
        separator.configure(padx=5, pady=5)
        self.row+=1

        # video control
        self.photo_init = PhotoImage(file = './init.png')
        self.frame_0 = Button(master, image=self.photo_init, command=self.prev_frame_callback, height = 30)
        self.frame_0.grid(row=self.row, column=0, padx=2, pady=4, sticky="wens")

        self.photo_pause = PhotoImage(file = './pause.png')
        self.pause = Button(master, image=self.photo_pause, command=self.prev_frame_callback, height = 30)
        self.pause.grid(row=self.row, column=1, padx=2, pady=4, sticky=W+E)

        self.photo_play = PhotoImage(file = './play.png')
        self.play = Button(master, image=self.photo_play, command=self.prev_frame_callback, height = 30)
        self.play.grid(row=self.row, column=2, padx=2, pady=4, sticky=W+E)

        self.photo_end = PhotoImage(file = './end.png')
        self.end = Button(master, image=self.photo_end, command=self.prev_frame_callback, height = 30)
        self.end.grid(row=self.row, column=3, padx=2, pady=4, sticky=W+E)
        self.row+=1

        self.prev_frame = Button(master, text='prev frame', command=self.prev_frame_callback)
        self.prev_frame.grid(row=self.row, column=0, padx=2, pady=10, sticky=W+E)
        self.next_frame = Button(master, text='next frame', command=self.next_frame_callback)
        self.next_frame.grid(row=self.row, column=1, padx=2, pady=10, sticky=W+E)
        self.prev_video = Button(master, text='prev video', command=self.prev_frame_callback)
        self.prev_video.grid(row=self.row, column=2, padx=2, pady=10, sticky=W+E)
        self.next_video = Button(master, text='next video', command=self.next_frame_callback)
        self.next_video.grid(row=self.row, column=3, padx=2, pady=10, sticky=W+E)
        self.row+=1

        # separator
        # self.L_empty = Label(master).grid(row=self.row,column=0, pady=2, padx=60, sticky=W+E)
        # self.row+=1
        separator = Frame(height=5, bd=1, relief=SUNKEN)
        separator.grid(row=self.row, columnspan=4, sticky="ew")
        separator.configure(padx=5, pady=15)
        self.row+=1

        # # region
        # collections = ("","")
        # Label(master, text="collections").grid(row=row, pady=10, sticky=W+E)
        # self.variable_r = StringVar(master)
        # self.variable_r.set(collections[0]) # default value
        # self.menu_folder = OptionMenu(master, self.variable_r, *collections)
        # self.menu_folder.grid(row=row, column=1, stick="ew")
        # self.menu_folder.configure(bg = "WHITE")  # Set background color to green
        # self.menu_folder.configure(activebackground = "LIGHTBLUE")  # Set background color to green
        # row+=1
        #
        # # start stop
        # Button(master, text="start", command=self.button_start_callback).grid(row=row, pady=3, sticky=W+E)
        # self.L_start = StringVar()
        # Label(master, textvariable=self.L_start).grid(row=row,column=1, pady=3, sticky=W+E)
        # row+=1
        # Button(master, text="stop", command=self.button_stop_callback).grid(row=row,  pady=3, sticky=W+E)
        # self.L_stop = StringVar()
        # Label(master, textvariable=self.L_stop).grid(row=row,column=1, pady=3, sticky=W+E)
        # row+=1
        #
        # # next and previous frames
        # Button(master, text="Next frame", command=self.next_f_callback).grid(row=row, column=0, pady=3, sticky=W+E)
        # Button(master, text="Prev frame", command=self.prev_f_callback).grid(row=row, column=1, pady=3, sticky=W+E)
        # row+=1
        #
        # # next and previous videos
        # Button(master, text="Next video", command=self.next_callback).grid(row=row, column=0, pady=3, sticky=W+E)
        # Button(master, text="Prev video", command=self.prev_callback).grid(row=row, column=1, pady=3, sticky=W+E)
        # row+=1
        #
        # # add label button
        # Button(master, text="Add action", command=self.add_callback).grid(row=row, column=0, pady=10, sticky=W+E, columnspan=2)
        # row+=1

        # empty labels
        self.L_empty = Label(master).grid(row=self.row,column=0, pady=100, padx=60, sticky=W+E)
        self.L_empty = Label(master).grid(row=self.row,column=1, pady=100, padx=60, sticky=W+E)
        self.L_empty = Label(master).grid(row=self.row,column=2, pady=100, padx=60, sticky=W+E)
        self.L_empty = Label(master).grid(row=self.row,column=3, pady=100, padx=60, sticky=W+E)
        self.row+=1
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

    def askdirectory(self):
        self.dir = tkFileDialog.askdirectory(**self.dir_opt)
        self.label_browse.configure(text = self.dir)

    def button_load_callback(self):
        if self.new_vid:
            r = self.variable_r.get()
            self.file_meta.write('region_id:'+str(self.RegionIDs[r])+'\n')
            self.file_meta.write('region:'+r+'\n')
            self.new_vid = 0
        act = ''

    def prev_frame_callback(self):
        self.scale_l.set(int(self.scale_l.get())-1)

    def next_frame_callback(self):
        self.scale_l.set(int(self.scale_l.get())+1)


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




#
# directory = '/home/omari/Datasets_old/Lucie/'
# date_files = [f for f in listdir(directory)]
# files_remaining = [f for f in date_files if not isfile(join(directory, f, "completed_labelling.txt"))]
# print files_remaining

def main():
    root = Tk()
    App(root)
    root.mainloop()

if __name__=="__main__":
    main()
