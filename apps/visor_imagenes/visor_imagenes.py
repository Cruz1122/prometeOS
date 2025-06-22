import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
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


class ImageViewer:
    """
    Image and video viewer application class
    """
    
    def __init__(self, root):
        """
        Initialize the image viewer application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Image and Video Viewer")
        self.root.iconbitmap(util.get_app_icon_path("visor_imagenes", "icon.ico"))
        self.root.geometry("1100x600")

        self.open_button = tk.Button(
            self.root, text="Open multimedia", command=self.open_image
        )
        self.open_button.pack(pady=20)

    def open_image(self):
        """Open dialog to select and view image or video files"""
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
        dialog.title("Select the image you want to open")
        dialog.iconbitmap(util.get_app_icon_path("visor_imagenes", "icon.ico"))
        dialog.geometry("500x300")

        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=1)

        for file in file_path:
            listbox.insert(tk.END, file)

        open_button = tk.Button(
            dialog,
            text="Open",
            command=lambda: self.open_selected_file(listbox, dialog),
        )
        open_button.pack()

    def open_selected_file(self, listbox, dialog):
        """
        Open the selected file using the system's default application
        
        Args:
            listbox: Listbox widget containing selected file
            dialog: Dialog window to close after opening file
        """
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
                messagebox.showerror("Error", f"Could not open the image: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
