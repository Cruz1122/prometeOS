import os
import tkinter as tk
from pygame import mixer
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="Directorio del usuario", type=str)
parser.add_argument("privilege", help="Nivel de privilegio del usuario", type=str)
args = parser.parse_args()

user_directory = args.user_directory

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de audio")
        self.root.iconbitmap("apps/reproductor_audio/icon.ico")
        self.root.configure(bg="#302939")

        # Centrar la ventana
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
        self.playlist = []

        # Título
        self.title = tk.Label(
            self.root,
            text="Reproductor de audio",
            font=("microsoftphagspa", 28, "bold"),
            bg="#302939",
            fg="white",
        )
        self.title.pack(pady=10)

        # Lista de reproducción
        self.playlist_box = tk.Listbox(
            self.root,
            bg="#493e57",
            fg="white",
            selectbackground="#e07171",
            selectforeground="white",
            font=("microsoftphagspa", 12),
        )
        self.playlist_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Controles de reproducción
        control_frame = tk.Frame(self.root, bg="#282828")
        control_frame.pack(pady=20)

        prev_btn = tk.Button(
            control_frame,
            text="Anterior",
            command=self.prev_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        prev_btn.grid(row=0, column=0, padx=10)

        play_btn = tk.Button(
            control_frame,
            text="Reproducir",
            command=self.play_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        play_btn.grid(row=0, column=1, padx=10)

        pause_btn = tk.Button(
            control_frame,
            text="Pausar",
            command=self.pause_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        pause_btn.grid(row=0, column=2, padx=10)

        next_btn = tk.Button(
            control_frame,
            text="Siguiente",
            command=self.next_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        next_btn.grid(row=0, column=3, padx=10)

        # Botón para eliminar canción
        remove_btn = tk.Button(
            control_frame,
            text="Eliminar",
            command=self.remove_song,
            bg="#e07171",
            fg="white",
            font=("microsoftphagspa", 12),
            width=10,
        )
        remove_btn.grid(row=0, column=4, padx=10)

        # Menú
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        add_song_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Archivo", menu=add_song_menu)
        add_song_menu.add_command(label="Agregar", command=self.add_songs)
        add_song_menu.add_command(label="Salir", command=self.root.quit)

    def add_songs(self):
        # Obtén una lista de todos los archivos en el directorio de música
        song_files = os.listdir(user_directory + "/music")
        # Filtra la lista para incluir solo los archivos .mp3
        song_files = [f for f in song_files if f.endswith(".mp3")]

        # Crea un nuevo cuadro de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccione las canciones que desee añadir a la lista")
        dialog.geometry("500x300")

        # Crea una lista en el cuadro de diálogo con los archivos de música
        listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE)
        listbox.pack(fill=tk.BOTH, expand=1)

        # Añade los archivos de música a la lista
        for song_file in song_files:
            listbox.insert(tk.END, song_file)

        # Añade un botón para añadir las canciones seleccionadas a la lista de reproducción
        add_button = tk.Button(dialog, text="Agregar", command=lambda: self.add_selected_songs(listbox, dialog))
        add_button.pack()

    def add_selected_songs(self, listbox, dialog):
        songs = [listbox.get(i) for i in listbox.curselection()]
        if songs:
            for song in songs:
                self.playlist.append(song)
                self.playlist_box.insert(tk.END, song)
        dialog.destroy()

    def remove_song(self):
        selected_song = self.playlist_box.curselection()[0]
        self.playlist_box.delete(selected_song)
        self.playlist.pop(selected_song)

    def play_song(self):
        if not self.playlist:
            return
        song = self.playlist[self.playlist_box.curselection()[0]]
        mixer.music.load(os.path.join(user_directory, "music", song))
        play_thread = threading.Thread(target=mixer.music.play)
        play_thread.start()

    def pause_song(self):
        if mixer.music.get_busy():
            mixer.music.pause()

    def next_song(self):
        current_selection = self.playlist_box.curselection()[0]
        next_selection = (current_selection + 1) % len(self.playlist)
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(next_selection)
        self.play_song()

    def prev_song(self):
        current_selection = self.playlist_box.curselection()[0]
        prev_selection = (current_selection - 1) % len(self.playlist)
        self.playlist_box.selection_clear(0, tk.END)
        self.playlist_box.selection_set(prev_selection)
        self.play_song()


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()
