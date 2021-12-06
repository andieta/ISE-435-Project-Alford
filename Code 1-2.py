# -*- coding: utf-8 -*-
"""
Author: Andrea Alford aalford2  ISE 435
MP3 Media Player
"""
#import the necessary tools
import os
import pickle
import pygame
import tkinter as kin
from tkinter import filedialog
from pygame import mixer


#create the class for the actual media player
class MP3Play(kin.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        mixer.init()
        
        if os.path.exists("musical.pickle"):
            with open("musical.pickle", "rb") as rem:
                self.musicList = pickle.load(rem)
        else:                
            self.musicList = []         #open a new list to put the music in
        
        
        #variables for later
        self.rightNow = 0
        self.stopped = True
        self.running = False
        
        
        ##run these functions
        self.windowFrm()
        self.track_fancyPrg()
        self.buttons_fancyPrg()
        self.listOTrack_fancyPrg()
        
        
    def windowFrm(self):        #function for the different parts of the window
        self.track = kin.LabelFrame(self, text = "Track", bg="purple", fg="white", bd=10, relief = kin.GROOVE)
        self.track.configure(width= 615, height = 375)
        self.track.grid(row=1, column= 0)
        
        self.listOTrack = kin.LabelFrame(self, text = "Song Library", bg="purple", fg="white", bd=10, relief = kin.GROOVE)
        self.listOTrack.configure(width= 380, height = 700)
        self.listOTrack.grid(row=0, column= 1, rowspan = 4)
        
        self.buttons = kin.LabelFrame(self, text = "Song Navigation", bg="purple", fg="white", bd=10, relief = kin.GROOVE)
        self.buttons.configure(width= 615, height = 375)
        self.buttons.grid(row=0, column= 0)
    
        
    def track_fancyPrg(self):
        self.canvas = kin.Label(self.track, bg="dark blue", fg="white", font=14)
        self.canvas["text"] = "Andie's Music Player"
        self.canvas.configure(width=35, height=2)
        self.canvas.grid(row=1, column=0)
    
    
    def buttons_fancyPrg(self):
        self.loadSongs = kin.Button(self.buttons, bg="dark green", fg="white", font=14)
        self.loadSongs["text"] = "Load Songs Here"
        self.loadSongs["command"]= self.getMusic  #insert the music fx to get folders
        self.loadSongs.grid(row=0, column=0)
        
        self.pauseNow= kin.Button(self.buttons, bg="#FFE5B4", fg="black", font=16)
        self.pauseNow["text"] = "play/pause"
        self.pauseNow["command"]= self.stopPlayback #insert the pause fx to stop/play
        self.pauseNow.grid(row=0, column=4)
        
        
        self.fwdSkip = kin.Button(self.buttons, bg="#FFE5B4", fg="black", font=16)
        self.fwdSkip["text"] = "next song"          #insert the skip fx to skip song
        self.fwdSkip["command"]= self.skipThisOne() 
        self.fwdSkip.grid(row=0, column=5)
        
        self.backSkip = kin.Button(self.buttons, bg="#FFE5B4", fg="black", font=16)
        self.backSkip["text"] = "prev song"
        self.backSkip["command"]= self.goBackOne()  #insert the previous fx to go back
        self.backSkip.grid(row=0, column=3)
        
        self.loudness = kin.DoubleVar()  #stores current volume
        self.slider = kin.Scale(self.buttons, from_ = 0, to = 50, orient = kin.HORIZONTAL)
        self.slider["variable"] = self.loudness
        self.slider.set(25)
        mixer.music.set_volume(0.5)
        self.slider["command"]= self.louderSofter
        self.slider.grid(row=0, column=6)
    
           
    def listOTrack_fancyPrg(self):
        self.scroll = kin.Scrollbar(self.listOTrack, orient = kin.VERTICAL)
        self.scroll.grid(row=0, column=1, rowspan= 10, sticky='ns')
        
        self.boxy= kin.Listbox(self.listOTrack, selectmode = kin.SINGLE, yscrollcommand = self.scroll.set, selectbackground= "pink")
        self.indexSongs()
        self.boxy.config(height=30)
        self.boxy.bind("<Double-1>", self.runItUp)
        self.scroll.config(command=self.boxy.yview)
        self.boxy.grid(row=0, column=0, rowspan=10)
        
      
    def indexSongs(self):
        for index, song in enumerate(self.musicList):
            self.boxy.insert(index, os.path.basename(song))  #basename to keep from getting long track names
        
       
    
    def getMusic(self):
        self.moreMusic = []
        folderLoc = filedialog.askdirectory()
        for root_, dirs, files in os.walk(folderLoc):
            for file in files:
                if os.path.splitext(file)[1]==".mp3":
                    path = (root_+ '/' + file).replace('\\', '/')
                    self.moreMusic.append(path)
        
        with open("musical.pickle", "wb") as rem: #overwirties the pickle file
            pickle.dump(self.moreMusic, rem)
        
        self.musicList = self.moreMusic
        self.boxy.delete(0, kin.END)
        self.indexSongs()
        
    def runItUp(self, event=None):
        if event is not None:
            self.rightNow = self.boxy.curselection()[0]
            for i in range(len(self.musicList)):
                self.boxy.itemconfigure(i, bg= "white")
        
        mixer.music.load(self.musicList[self.rightNow])
        
        self.stopped = False
        self.running = True
        self.canvas["anchor"] = "w"
        self.canvas["text"] = os.path.basename(self.musicList[self.rightNow])
        self.boxy.activate(self.rightNow)
        self.boxy.itemconfigure(self.rightNow, bg="white")
        mixer.music.play()
        
        
    def stopPlayback(self):
        if not self.stopped:
            self.stopped = True
            mixer.music.pause()
        else:
            if self.running == False:
                self.runItUp()
            self.stopped = False
            mixer.music.unpause()
            
    
    def goBackOne(self):
        pass
    
    def skipThisOne(self):
        pass
    
  
    def louderSofter(self, event=None):
        self.v = self.loudness.get()
        print(self.v)
        mixer.music.set_volume(self.v /50)
      
         
#create a variable to call tk easily
based = kin.Tk()
based.geometry("1200x750")  #the way the app will look in size
based.title("Andie's Music Player")


interfaced = MP3Play(master = based)
interfaced.mainloop()