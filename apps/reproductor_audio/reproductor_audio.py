import os
import tkinter as tk
from pygame import mixer
import threading
import argparse
import sys

# Add the project root directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_dir)

import utilities.generic as util

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="User directory", type=str)
parser.add_argument("privilege", help="User privilege level", type=str)
args = parser.parse_args()

user_directory = args.user_directory


class AudioPlayer:
    """
    Audio player application class that provides music playback functionality
    """
    
    def __init__(self, root):
        """
        Initialize the audio player application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Audio Player")
        self.root.iconbitmap(util.get_app_icon_path("reproductor_audio", "icon.ico"))
        self.root.configure(bg="#302939")

        # Center the window
        window_width = 1100
        window_height = 600

        position_top = int(
            self.root.winfo_screenheight() / 2 - self.root.winfo_screenheight() / 2
        )
        position_right = int(
            self.root.winfo_screenwidth() / 2 - self.root.winfo_screenwidth() / 2
        )
        self.root.geometry(
            f"{window_width}x{window_height}+{position_right}+{position_top}"
        )

        mixer.init()

        self.create_widgets()

    def create_widgets(self):
        """Create and configure the audio player interface widgets"""
        self.playlist = []

        # Title
        self.title = tk.Label(
            self.root,
            text="Audio Player",
            font=("microsoftphagspa", 28, "bold"),
            bg="#302939",
            fg="white",
        )
        self.title.pack(pady=10)

        # Playlist
        self.playlist_box = tk.Listbox(
            self.root,
            bg="#493e57",
            fg="white",
            selectbackground="#e07171",
            selectforeground="white",
            font=("microsoftphagspa", 12),
        )
        self.playlist_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Playback controls
        control_frame = tk.Frame(self.root, bg="#282828")
        control_frame.pack(pady=20)

        prev_btn = tk.Button(
            control_frame,
            text="Previous",
            command=self.prev_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        prev_btn.grid(row=0, column=0, padx=10)

        play_btn = tk.Button(
            control_frame,
            text="Play",
            command=self.play_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        play_btn.grid(row=0, column=1, padx=10)

        pause_btn = tk.Button(
            control_frame,
            text="Pause",
            command=self.pause_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        pause_btn.grid(row=0, column=2, padx=10)

        next_btn = tk.Button(
            control_frame,
            text="Next",
            command=self.next_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        next_btn.grid(row=0, column=3, padx=10)

        # Remove song button
        remove_btn = tk.Button(
            control_frame,
            text="Remove",
            command=self.remove_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        remove_btn.grid(row=0, column=4, padx=10)

        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        add_song_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=add_song_menu)
        add_song_menu.add_command(label="Add", command=self.add_songs)
        add_song_menu.add_command(label="Exit", command=self.root.quit)

    def add_songs(self):
        """Open dialog to select songs to add to playlist"""
        song_files = os.listdir(user_directory + "/music")
        song_files = [f for f in song_files if f.endswith(".mp3")]

        dialog = tk.Toplevel(self.root)
        dialog.title("Select the songs you want to add to the playlist")
        dialog.iconbitmap(util.get_app_icon_path("reproductor_audio", "icon.ico"))
        dialog.geometry("500x300")

        listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE)
        listbox.pack(fill=tk.BOTH, expand=1)

        for song_file in song_files:
            listbox.insert(tk.END, song_file)

        add_button = tk.Button(dialog, text="Add", command=lambda: self.add_selected_songs(listbox, dialog))
        add_button.pack()

    def add_selected_songs(self, listbox, dialog):
        """
        Add selected songs from dialog to playlist
        
        Args:
            listbox: Listbox widget containing selected songs
            dialog: Dialog window to close after adding songs
        """
        songs = [listbox.get(i) for i in listbox.curselection()]
        if songs:
            for song in songs:
                self.playlist.append(song)
                self.playlist_box.insert(tk.END, song)
        dialog.destroy()

    def remove_song(self):
        """Remove selected song from playlist"""
        selected_song = self.playlist_box.curselection()[0]
        self.playlist_box.delete(selected_song)
        self.playlist.pop(selected_song)

    def play_song(self):
        """Play the currently selected song"""
        if not self.playlist:
            return
        song = self.playlist[self.playlist_box.curselection()[0]]
        mixer.music.load(os.path.join(user_directory, "music", song))
        play_thread = threading.Thread(target=mixer.music.play)
        play_thread.start()

    def pause_song(self):
        """Pause the currently playing song"""
        if mixer.music.get_busy():
            mixer.music.pause()

    def next_song(self):
        """Play the next song in the playlist"""
        current_selection = self.playlist_box.curselection()[0]
        next_selection = (current_selection + 1) % len(self.playlist)
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(next_selection)
        self.play_song()

    def prev_song(self):
        """Play the previous song in the playlist"""
        current_selection = self.playlist_box.curselection()[0]
        prev_selection = (current_selection - 1) % len(self.playlist)
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(prev_selection)
        self.play_song()


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()
