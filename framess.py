import tkinter as tk
import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black", highlightbackground="black", highlightthickness=2)
        self.master = master
        self.pack()
        self.create_frames()
        self.playlist = []
        
    def create_frames(self):
        self.track = tk.LabelFrame(self, text='Track', 
                    font=("times new roman",15,"bold"),
                    bg="#0D3F70",fg="white",bd=5,relief=tk.GROOVE)
        self.track.config(width=437,height=370)
        self.track.grid(row=0, column=0,padx=3)

        self.tracklist = tk.LabelFrame(self,text='Playlist',
                            font=("times new roman",15,"bold"),
                            bg="#002347",fg="white",bd=5,relief=tk.GROOVE)
        self.tracklist.config(width=210,height=370)
        self.tracklist.grid(row=0, column=1, pady=3, padx=2)

        self.controls = tk.LabelFrame(self,
                            font=("times new roman",15,"bold"),
                            bg="#002347",fg="white",bd=2,relief=tk.GROOVE)
        self.controls.config(width=652,height=55)
        self.controls.grid(row=1, column=0,columnspan=2, pady=3)

        
        
root = tk.Tk()
root.geometry('680x440')
root.wm_title('Musicly Player')
root.configure(bg='black')  

app = Player(master=root)
app.mainloop()