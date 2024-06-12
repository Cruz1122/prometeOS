import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import argparse
import shutil
from tkinter import simpledialog

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="Directorio del usuario", type=str)
parser.add_argument("privilege", help="Nivel de privilegio del usuario", type=str)
args = parser.parse_args()

user_directory = args.user_directory
privilege = int(args.privilege)


class FileManager:
    def __init__(self, root, user_directory):
        self.root = root
        self.user_directory = user_directory
        self.current_directory = user_directory
        self.copied_item = None

        self.root.title("Administrador de archivos")
        self.root.iconbitmap("apps/explorador_archivos/icon.ico")

        # Centrar la ventana
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
        self.tree.heading("#0", text="Nombre")
        self.tree.heading("size", text="Tamaño")
        self.tree.heading("modified", text="Última modificación")
        self.tree.column("#0", stretch=tk.YES)
        self.tree.column("size", stretch=tk.YES)
        self.tree.column("modified", stretch=tk.YES)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

        self.load_directory(self.current_directory)

    def load_directory(self, directory):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Crear un elemento para navegar al directorio padre
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
                    "Advertencia", "No puede navegar fuera del directorio base."
                )
        else:
            messagebox.showinfo(
                "Información del Archivo", f"Has seleccionado el archivo: {path}"
            )

    def on_right_click(self, event):
        item = self.tree.identify_row(event.y)
        self.tree.selection_set(item)

        if privilege > 1:
            if self.tree.item(item, "tags"):
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Cambiar nombre", command=self.rename_item)
                menu.add_command(label="Eliminar", command=self.delete_item)
                menu.add_command(label="Copiar", command=self.copy_item)
                menu.post(event.x_root, event.y_root)
            else:
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(label="Pegar", command=self.paste_item)
                menu.add_command(label="Crear", command=self.create_item)
                menu.post(event.x_root, event.y_root)

    def rename_item(self):
        item = self.tree.selection()[0]
        old_name = self.tree.item(item, "text")
        old_path = os.path.join(self.current_directory, old_name)

        new_name = simpledialog.askstring(
            "Cambiar Nombre", "Ingrese el nuevo nombre:", initialvalue=old_name
        )
        if new_name:
            new_path = os.path.join(self.current_directory, new_name)
            os.rename(old_path, new_path)
            self.load_directory(self.current_directory)

    def create_item(self):
        name = simpledialog.askstring("Crear", "Ingrese el nombre del archivo o carpeta:")
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
                messagebox.showerror("Error", "El archivo o carpeta ya existe.")

    def delete_item(self):
        item = self.tree.selection()[0]
        name = self.tree.item(item, "text")
        path = os.path.join(self.current_directory, name)

        confirm = messagebox.askyesno("Eliminar", f"¿Está seguro de eliminar '{name}'?")
        if confirm:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.load_directory(self.current_directory)

    def copy_item(self):
        item = self.tree.selection()[0]
        self.copied_item = os.path.join(
            self.current_directory, self.tree.item(item, "text")
        )

    def paste_item(self):
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
        import time

        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


if __name__ == "__main__":
    root = tk.Tk()
    file_manager = FileManager(root, user_directory)
    root.mainloop()
