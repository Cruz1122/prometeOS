import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import argparse
import shutil
from tkinter import simpledialog
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
privilege = int(args.privilege)


class FileManager:
    """
    File manager application class that provides file and directory management
    """
    
    def __init__(self, root, user_directory):
        """
        Initialize the file manager application
        
        Args:
            root: Tkinter root window
            user_directory: User's home directory
        """
        self.root = root
        self.user_directory = user_directory
        self.current_directory = user_directory
        self.copied_item = None

        self.root.title("File Manager")
        self.root.iconbitmap(util.get_app_icon_path("explorador_archivos", "icon.ico"))

        # Center the window
        window_width = 1100
        window_height = 600
        position_top = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        self.root.geometry(
            f"{window_width}x{window_height}+{position_right}+{position_top}"
        )

        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            foreground="#e07171",
            font=("microsoftphagspa", 10, "bold"),
        )

        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.frame, columns=("size", "modified"))
        self.tree.heading("#0", text="Name")
        self.tree.heading("size", text="Size")
        self.tree.heading("modified", text="Last Modified")
        self.tree.column("#0", stretch=tk.YES)
        self.tree.column("size", stretch=tk.YES)
        self.tree.column("modified", stretch=tk.YES)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

        self.load_directory(self.current_directory)

    def load_directory(self, directory):
        """
        Load and display the contents of a directory
        
        Args:
            directory (str): Path to the directory to load
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Create an element to navigate to parent directory
        if directory != self.user_directory:
            self.tree.insert("", tk.END, text="..", values=("", ""))

        for entry in os.scandir(directory):
            name = entry.name
            is_dir = entry.is_dir()
            size = entry.stat().st_size
            modified = entry.stat().st_mtime

            values = (f"{size} bytes", self.format_time(modified))
            self.tree.insert(
                "",
                tk.END,
                text=name,
                values=values,
                tags=("dir",) if is_dir else ("file",),
            )

    def on_double_click(self, event):
        """Handle double-click events on tree items"""
        item = self.tree.selection()[0]
        name = self.tree.item(item, "text")
        path = os.path.join(self.current_directory, name)

        if name == "..":
            self.current_directory = os.path.dirname(self.current_directory)
            self.load_directory(self.current_directory)

        elif os.path.isdir(path):
            if path.startswith(self.user_directory):
                self.current_directory = path
                self.load_directory(self.current_directory)
            else:
                messagebox.showwarning(
                    "Warning", "You cannot navigate outside the base directory."
                )
        else:
            messagebox.showinfo(
                "File Information", f"You have selected the file: {path}"
            )

    def on_right_click(self, event):
        """Handle right-click events to show context menu"""
        item = self.tree.identify_row(event.y)
        self.tree.selection_set(item)

        if privilege > 1:
            if self.tree.item(item, "tags"):
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Rename", command=self.rename_item)
                menu.add_command(label="Delete", command=self.delete_item)
                menu.add_command(label="Copy", command=self.copy_item)
                menu.post(event.x_root, event.y_root)
            else:
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Paste", command=self.paste_item)
                menu.add_command(label="Create", command=self.create_item)
                menu.post(event.x_root, event.y_root)

    def rename_item(self):
        """Rename the selected file or directory"""
        item = self.tree.selection()[0]
        old_name = self.tree.item(item, "text")
        old_path = os.path.join(self.current_directory, old_name)

        new_name = simpledialog.askstring(
            "Rename", "Enter the new name:", initialvalue=old_name
        )
        if new_name:
            new_path = os.path.join(self.current_directory, new_name)
            os.rename(old_path, new_path)
            self.load_directory(self.current_directory)

    def create_item(self):
        """Create a new file or directory"""
        name = simpledialog.askstring("Create", "Enter the name of the file or folder:")
        if name:
            path = os.path.join(self.current_directory, name)
            if not os.path.exists(path):
                if name.endswith(".txt"):
                    with open(path, "w") as file:
                        pass
                else:
                    os.makedirs(path, exist_ok=True)
                self.load_directory(self.current_directory)
            else:
                messagebox.showerror("Error", "The file or folder already exists.")

    def delete_item(self):
        """Delete the selected file or directory"""
        item = self.tree.selection()[0]
        name = self.tree.item(item, "text")
        path = os.path.join(self.current_directory, name)

        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.load_directory(self.current_directory)

    def copy_item(self):
        """Copy the selected item to clipboard"""
        item = self.tree.selection()[0]
        self.copied_item = os.path.join(
            self.current_directory, self.tree.item(item, "text")
        )

    def paste_item(self):
        """Paste the copied item to current directory"""
        if self.copied_item:
            new_path = os.path.join(
                self.current_directory, os.path.basename(self.copied_item)
            )
            if os.path.isdir(self.copied_item):
                shutil.copytree(self.copied_item, new_path)
            else:
                shutil.copy2(self.copied_item, new_path)
            self.load_directory(self.current_directory)

    def format_time(self, timestamp):
        """
        Format timestamp to readable string
        
        Args:
            timestamp (float): Unix timestamp
            
        Returns:
            str: Formatted time string
        """
        import time

        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


if __name__ == "__main__":
    root = tk.Tk()
    file_manager = FileManager(root, user_directory)
    root.mainloop()
