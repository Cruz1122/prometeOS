import tkinter as tk
from tkinter import filedialog, messagebox
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


class Notepad:
    """
    Notepad application class that provides basic text editing functionality
    """
    
    def __init__(self, root):
        """
        Initialize the notepad application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Notepad")
        self.root.iconbitmap(util.get_app_icon_path("bloc_notas", "icon.ico"))
        self.root.geometry("1100x600")

        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cut",
            command=lambda: self.root.focus_get().event_generate("<<Cut>>"),
        )
        edit_menu.add_command(
            label="Copy",
            command=lambda: self.root.focus_get().event_generate("<<Copy>>"),
        )
        edit_menu.add_command(
            label="Paste",
            command=lambda: self.root.focus_get().event_generate("<<Paste>>"),
        )
        edit_menu.add_command(
            label="Select All",
            command=lambda: self.text_area.tag_add("sel", "1.0", "end"),
        )

        self.current_file = None

    def new_file(self):
        """Create a new file"""
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Notepad - New File")

    def open_file(self):
        """Open file dialog to select a file to open"""
        file_path = os.listdir(user_directory + "/documents")
        file_path = [f for f in file_path if f.endswith(".txt")]

        dialog = tk.Toplevel(self.root)
        dialog.title("Select the file you want to open")
        dialog.iconbitmap(util.get_app_icon_path("bloc_notas", "icon.ico"))
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
        Open the selected file from the listbox
        
        Args:
            listbox: Listbox widget containing file names
            dialog: Dialog window to close after opening file
        """
        file = listbox.get(listbox.curselection())
        if file:
            self.current_file = file
            self.root.title(f"Notepad - {os.path.basename(file)}")
            with open(
                os.path.join(user_directory, "documents", file), "r", encoding="utf-8"
            ) as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
        dialog.destroy()

    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                with open(
                    os.path.join(user_directory, "documents", self.current_file),
                    "w",
                    encoding="utf-8",
                ) as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    messagebox.showinfo(
                        "Save File", "File saved successfully"
                    )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not save file: {str(e)}"
                )
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save file with a new name"""
        file = filedialog.asksaveasfilename(
            initialdir=os.path.join(user_directory, "documents"),
            title="Save File",
            filetypes=(("Text Files", "*.txt"), ("All files", "*.*")),
        )
        if file:
            self.current_file = os.path.basename(file)
            self.root.title(f"Notepad - {os.path.basename(file)}")
            with open(file, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Save File", "File saved successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()
