import tkinter as tk
from tkinter import filedialog, messagebox
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="Directorio del usuario", type=str)
parser.add_argument("privilege", help="Nivel de privilegio del usuario", type=str)
args = parser.parse_args()

user_directory = args.user_directory


class BlocNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloc de Notas")
        self.root.iconbitmap("apps/bloc_notas/icon.ico")
        self.root.geometry("1100x600")

        self.text_area = tk.Text(self.root, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Deshacer", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Rehacer", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cortar",
            command=lambda: self.root.focus_get().event_generate("<<Cut>>"),
        )
        edit_menu.add_command(
            label="Copiar",
            command=lambda: self.root.focus_get().event_generate("<<Copy>>"),
        )
        edit_menu.add_command(
            label="Pegar",
            command=lambda: self.root.focus_get().event_generate("<<Paste>>"),
        )
        edit_menu.add_command(
            label="Seleccionar Todo",
            command=lambda: self.text_area.tag_add("sel", "1.0", "end"),
        )

        self.current_file = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Bloc de Notas - Nuevo Archivo")

    def open_file(self):
        file_path = os.listdir(user_directory + "/documents")
        file_path = [f for f in file_path if f.endswith(".txt")]

        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccione el archivo que desea abrir")
        dialog.iconbitmap("apps/bloc_notas/icon.ico")
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
            self.current_file = file
            self.root.title(f"Bloc de Notas - {os.path.basename(file)}")
            with open(
                os.path.join(user_directory, "documents", file), "r", encoding="utf-8"
            ) as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
        dialog.destroy()

    def save_file(self):
        if self.current_file:
            try:
                with open(
                    os.path.join(user_directory, "documents", self.current_file),
                    "w",
                    encoding="utf-8",
                ) as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    messagebox.showinfo(
                        "Guardar Archivo", "Archivo guardado correctamente"
                    )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo guardar el archivo: {str(e)}"
                )
        else:
            self.save_file_as()

    def save_file_as(self):
        file = filedialog.asksaveasfilename(
            initialdir=os.path.join(user_directory, "documents"),
            title="Guardar Archivo",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if file:
            self.current_file = os.path.basename(file)
            self.root.title(f"Bloc de Notas - {os.path.basename(file)}")
            with open(file, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Guardar Archivo", "Archivo guardado correctamente")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlocNotas(root)
    root.mainloop()
