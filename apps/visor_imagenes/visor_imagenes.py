import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="Directorio del usuario", type=str)
parser.add_argument("privilege", help="Nivel de privilegio del usuario", type=str)
args = parser.parse_args()

user_directory = args.user_directory


class VisorImagenes:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de imágenes y videos")
        self.root.iconbitmap("apps/visor_imagenes/icon.ico")
        self.root.geometry("1100x600")

        self.open_button = tk.Button(
            self.root, text="Abrir multimedia", command=self.open_image
        )
        self.open_button.pack(pady=20)

    def open_image(self):
        file_path = os.listdir(user_directory + "/media")
        print(file_path)
        file_path = [
            f
            for f in file_path
            if f.endswith(".png")
            or f.endswith(".jpg")
            or f.endswith(".jpeg")
            or f.endswith(".bmp")
            or f.endswith(".gif")
            or f.endswith(".mp4")
            or f.endswith(".avi")
            or f.endswith(".mkv")
        ]

        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccione la imagen que desea abrir")
        dialog.iconbitmap("apps/visor_imagenes/icon.ico")
        dialog.geometry("500x300")

        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=1)

        for file in file_path:
            listbox.insert(tk.END, file)

        open_button = tk.Button(
            dialog,
            text="Abrir",
            command=lambda: self.open_selected_file(listbox, dialog),
        )
        open_button.pack()

    def open_selected_file(self, listbox, dialog):
        file = listbox.get(listbox.curselection())
        if file:
            try:
                if os.name == "nt":  # Windows
                    os.startfile(os.path.join(user_directory, "media", file))
                elif os.name == "posix":  # macOS, Linux
                    subprocess.run(
                        ["open", os.path.join(user_directory, "media", file)]
                    )
                elif os.uname().sysname == "Linux":
                    subprocess.run(
                        ["xdg-open", os.path.join(user_directory, "media", file)]
                    )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la imagen: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VisorImagenes(root)
    root.mainloop()
