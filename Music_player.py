import tkinter as tk
from tkinter import filedialog, PhotoImage,messagebox
import os
import pygame.mixer as mixer
from tkinter import ttk
from mutagen.mp3 import MP3
import time
import shutil

class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="black", highlightbackground="black", highlightthickness=2)
        self.master = master
        self.pack()

        default_songs = [
            "Music/Bollywood/Aashiq Tera.mp3",
            "Music/Bollywood/Apna Bana Le.mp3",
            "Music/Bollywood/Blue Eyes.mp3",
            "Music/Bollywood/Chaleya.mp3",
            "Music/Bollywood/Challa.mp3",
            "Music/Bollywood/Criminal.mp3",
            "Music/Bollywood/Dafa 406.mp3",
            "Music/Bollywood/Ek Pal Ka Jeena.mp3 ",
            "Music/Bollywood/Ilahi - Arijit Singh.mp3",
            "Music/Bollywood/Ishq Shava.mp3",
            "Music/Bollywood/Kabhi Kabhi Aditi.mp3",
            "Music/Bollywood/khairiyat.mp3",
            "Music/Bollywood/Khalasi.mp3",
            "Music/Bollywood/Naacho Naacho - RRR.mp3",
            "Music/Bollywood/Sab Tera - Baaghi.mp3",
            "Music/Bollywood/Tum Hi Aana - Marjaavaan.mp3",
            "Music/Bollywood/Ude Dil Befikre.mp3",
            "Music/Bollywood/Udhal Ho - Malaal.mp3",
            "Music/Bollywood/Uska Hi Banana.mp3",
            "Music/Bollywood/Ved Tujha - Ved.mp3"
        ]
        
        self.playlist = default_songs
        self.image_paths = ["images/aashiq tera.gif",
                            "images/apna banale.gif",
                            "images/blue eyes.gif",
                            "images/chaleya.gif",
                            "images/challa.gif",
                            "images/criminal.gif",
                            "images/Dafa 4066.gif",
                            "images/ek pal.gif", 
                            "images/ilahi.gif",
                            "images/ishq Shava.gif",
                            "images/kabhi kabhi aditii.gif",
                            "images/khairiyatt.gif",
                            "images/khalasi.gif",
                            "images/nacho nacho.gif",
                            "images/sab tera.gif",
                            "images/marjaavaan.gif",
                            "images/ude dil.gif",
                            "images/udhal hoo.gif",
                            "images/1920.gif",
                            "images/ved tujhaaaaa.gif"
                            ]
        self.current_song_index = 0
        self.current_position = 0

        mixer.init()
        self.create_frames()
        self.track_widgets()
        self.controls_widgets()
        self.tracklist_widgets()
        self.playing = False
        self.paused = False
        self.update_playlist()

        self.song_length = 0
        self.current_time = 0
        self.update_progress_bar()

        self.start_time = 0  # Added for tracking start time when pausing

    def create_frames(self):
        self.track = tk.LabelFrame(self, text='Track',
                                   font=("times new roman", 15, "bold","italic"),
                                   bg="#0c0c0c", fg="#FF7373", bd=3, relief=tk.GROOVE,highlightcolor="#FF7373",highlightbackground="#FF7373")
        self.track.config(width=437, height=370)
        self.track.grid(row=0, column=0, padx=3)

        self.tracklist = tk.LabelFrame(self, text='Playlist',
                                       font=("times new roman", 15, "bold","italic"),
                                       bg="#0c0c0c", fg="#FF7373", bd=3, relief=tk.GROOVE)
        self.tracklist.config(width=210, height=374)
        self.tracklist.grid(row=0, column=1, pady=3, padx=2)

        self.controls = tk.LabelFrame(self,
                                      font=("times new roman", 15, "bold"),
                                      bg="#0c0c0c", fg="white", bd=2, relief=tk.GROOVE)
        self.controls.config(width=620, height=55)
        self.controls.grid(row=1, column=0, columnspan=2, pady=3)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=437, height=295)
        self.canvas.grid(row=0, column=0)

        self.songtrack = tk.Label(self.track, font=("times new roman", 16, "bold","italic"),
                                  bg="white", fg="#8D000E")
        self.songtrack['text'] = 'Musicly MP3 Player'
        self.songtrack.config(width=32, height=1)
        self.songtrack.grid(row=1, column=0, padx=10, pady=6)

    def controls_widgets(self):
        self.prev = tk.Button(self.controls, image=prev, bd=0, highlightthickness=0, borderwidth=0,
                              command=self.prev_music)
        self.prev.grid(row=0, column=0, padx=4, pady=9.5)

        self.play = tk.Button(self.controls, image=play, bd=0, highlightthickness=0, borderwidth=0,
                              command=self.toggle_play)
        self.play.grid(row=0, column=1, padx=2)

        self.next = tk.Button(self.controls, image=next, bd=0, highlightthickness=0, borderwidth=0,
                              command=self.next_music)
        self.next.grid(row=0, column=2, padx=2)

        self.progress_label = tk.Label(self.controls, text="00:00", font=("times new roman", 12, "bold"),
                                       bg="#0c0c0c", fg="#fefdfd")
        self.progress_label.grid(row=0, column=3, padx=4)

        self.progress_bar_style = ttk.Style()
        self.progress_bar_style.configure("TProgressbar",
                                  thickness=10, bordercolor="#003366",
                                  troughrelief=tk.FLAT, troughanchor="w",
                                  troughcolor="#0c0c0c",  # Trough (background) color
                                  barcolor="black")     # Bar (inside progress) color

        self.progress_bar = ttk.Progressbar(self.controls, orient=tk.HORIZONTAL, mode='determinate', length=330,
                                    maximum=100, value=0, style="TProgressbar")
        self.progress_bar.grid(row=0, column=4, padx=1)

        self.volume = tk.DoubleVar(self, value=0.5)
        self.volume_button = tk.Label(self.controls, text=f'Vol{int(self.volume.get() * 100)}%',
                                      font=("times new roman", 10, "bold"),
                                      bg="#0c0c0c", fg="#fefdfd")
        self.volume_button.grid(row=0, column=5, padx=3)

        self.volume_down = tk.Button(self.controls, text="-", font=("times new roman", 13, "bold"),
                                     bg="#0c0c0c", fg="#FF7373", command=self.volume_down,
                                     activebackground="#0c0c0c", activeforeground="#FF7373")
        self.volume_down.grid(row=0, column=6, padx=3)
        
        self.volume_up = tk.Button(self.controls, text="+", font=("times new roman", 12, "bold"),
                                   bg="#0c0c0c", fg="#FF7373", command=self.volume_up,
                                   activebackground="#0c0c0c", activeforeground="#FF7373")
        self.volume_up.grid(row=0, column=7, padx=3)


        self.download = tk.Button(self.controls, image=download, bd=0, highlightthickness=0, borderwidth=0,
                                  command=self.download_current_song)
        self.download.grid(row=0, column=8, padx=6)

    def tracklist_widgets(self):
        self.listbox = tk.Listbox(self.tracklist, selectbackground="#0c0c0c", selectmode=tk.SINGLE,
                                  font=("times new roman", 13), bg="#0c0c0c", fg="#fefdfd", highlightthickness=0,
                                  relief=tk.GROOVE, height=17, width=22, bd=0)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listbox.bind('<<ListboxSelect>>', self.play_selected_song)


    def update_progress_bar(self):
        if not self.paused and self.playing:
            self.current_time = mixer.music.get_pos() // 1000

            if self.song_length > 0:
                time_remaining = max(self.song_length - self.current_time, 0)
                self.progress_label['text'] = f"{time.strftime('%M:%S', time.gmtime(time_remaining))}"
                self.progress_bar['value'] = self.current_time
                

        self.after(1000, self.update_progress_bar)

    def update_playlist(self):
        self.listbox.delete(0, tk.END)

        for song_path in self.playlist:
            song_name = os.path.basename(song_path)
            song_name_with_space = f' {song_name}'  # Add a space before the song name
            self.listbox.insert(tk.END, song_name_with_space)
        
    def play_selected_song(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_song_index = selected_index[0]
            self.play_music()

    def play_music(self):
        if self.playlist:
            current_song = self.playlist[self.current_song_index]
            self.stop_music()
            mixer.music.load(current_song)

            if not self.paused:
                self.start_time = time.time()

            mixer.music.play(start=0)  # Start from the beginning
            self.current_position = 0  # Reset current position for a new song

            self.song_length = MP3(current_song).info.length
            self.progress_bar['maximum'] = self.song_length
            self.songtrack['text'] = os.path.basename(current_song)
            self.update_image()
            self.playing = True
            self.paused = False  # Reset paused flag
            self.play.config(image=pause) 



    def stop_music(self):
        mixer.music.stop()
        self.current_position = 0  # Reset current position when stopping the music


    def pause_music(self):
        if self.playing and not self.paused:
            mixer.music.pause()
            self.paused = True
            self.playing = False
            self.play.config(image=play)  # Change pause button to play
            self.current_position = time.time() - self.start_time

    def prev_music(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play_music()
            
            # Update the selection in the playlist
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_song_index)
            self.listbox.activate(self.current_song_index)
            self.listbox.see(self.current_song_index)


    def next_music(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.play_music()
            
            # Update the selection in the playlist
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_song_index)
            self.listbox.activate(self.current_song_index)
            self.listbox.see(self.current_song_index)

    def toggle_play(self):
        if self.playing:
            self.pause_music()
        else:
            self.resume_music()

    def resume_music(self):
        if self.paused:
            mixer.music.unpause()
            self.playing = True
            self.paused = False
            self.play.config(image=pause)  # Change play button to pause
            self.start_time = time.time() - self.current_position  # Change play button to pause

    def volume_up(self):
        current_volume = self.volume.get()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.01, 1.0)
            self.set_volume(new_volume)

    def volume_down(self):
        current_volume = self.volume.get()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.01, 0.0)
            self.set_volume(new_volume)

    def set_volume(self, volume):
        self.volume.set(volume)
        mixer.music.set_volume(volume)
        self.update_volume_label()

    def update_volume_label(self):
        self.volume_button['text'] = f'Vol  {int(self.volume.get() * 100)}'
        self.volume_button['font'] = ("times new roman", 12, "bold")

    def update_image(self):
        current_image_path = self.image_paths[self.current_song_index]
        new_image = PhotoImage(file=current_image_path)
        self.canvas.destroy()
        self.canvas = tk.Label(self.track, image=new_image)
        self.canvas.configure(width=437, height=295)
        self.canvas.grid(row=0, column=0)
        self.canvas.image = new_image
        self.canvas.update()
        

    def download_song(self, path):
        destination = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if destination:
            shutil.copyfile(path, destination)
            message_window = tk.Toplevel(self.master)
            message_window.title("Download Status")
            message_window.config(bg='black')
            message_window.geometry("280x50")

            message_label = tk.Label(message_window, text="Song Downloaded Successfully !", font=("times new roman", 12, "bold","italic"), pady=10, fg='#FF7373', bg='black')
            message_label.pack()
            window_width = message_window.winfo_reqwidth()
            window_height = message_window.winfo_reqheight()
            x_coordinate = int(self.master.winfo_x() + (self.master.winfo_width() / 2) - (window_width / 2))
            y_coordinate = int(self.master.winfo_y() + (self.master.winfo_height() / 2) - (window_height / 2))
            message_window.geometry(f"+{x_coordinate}+{y_coordinate}")
            message_window.resizable(False, False)

    def download_current_song(self):
        if self.playlist:
            current_song_path = self.playlist[self.current_song_index]
            self.download_song(current_song_path)

root = tk.Tk()
root.geometry('678x442')
root.wm_title('Musicly Player')
root.configure(bg='black')
root.config(pady=2)
root.resizable(False, False) 

img = PhotoImage(file='images/guitar.gif')
next = PhotoImage(file='images/nexticon1.gif')
prev = PhotoImage(file='images/previousicon1.gif')
pause = PhotoImage(file='images/pauseicon1.gif')
play = PhotoImage(file='images/playicon1.gif')  # Added play icon here
download = PhotoImage(file='images/downloadicon1.gif')

app = Player(master=root)
app.update_volume_label()
app.mainloop()
