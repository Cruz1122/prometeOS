import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter.font import BOLD
import utilities.generic as util
from forms.form_desktop import Escritorio
from forms.form_login import Login


class Register:
    def verify_register(self):
        user = self.usuario.get()
        password = self.password.get()
        password1 = self.password1.get()
        names = self.names.get()
        lastnames = self.lastnames.get()
        foto_perfil = self.profile_picture

        if password != password1:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # Verificar si los campos no están vacíos
        if not user or not password or not names or not lastnames:
            messagebox.showerror("Error", "Por favor, llene todos los campos")
            return

        if not os.path.exists("users.json"):
            with open("users.json", "w") as file:
                json.dump({}, file)
                self.nivel_privilegio = 3
        with open("users.json", "r") as file:
            users = json.load(file)

        if user in users:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        users[user] = {
            "username": user,
            "password": util.code_password(password),
            "names": names,
            "lastnames": lastnames,
            "profile_picture": foto_perfil,
            "wallpaper": self.fondo_pantalla,
            "privilege": self.nivel_privilegio,
            "apps": self.apps
        }

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        # Crear carpeta para el usuario en /users
        user_dir = os.path.join("..", "users", user)
        print(user_dir)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)  # Crea la carpeta del usuario

        # Crear subcarpetas
        os.makedirs(os.path.join(user_dir, "music"), exist_ok=True)
        os.makedirs(os.path.join(user_dir, "media"), exist_ok=True)
        os.makedirs(os.path.join(user_dir, "documents"), exist_ok=True)

        self.window.destroy()
        Login()

    def select_profile(self):
        self.profile_picture = filedialog.askopenfilename(initialdir="./media/pictures/fotos_perfil", title="Seleccione una foto de perfil",
                                                      defaultextension=".png")

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PrometeOS - Crear cuenta")
        self.window.geometry("800x800")
        self.window.config(bg=util.Colors.white)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap(os.path.join(".", "media", "icons", "logo.ico"))
        util.center_window(self.window, 800, 800)

        logo = util.load_image(
            os.path.join(".", "media", "pictures", "logo.png"), (200, 200)
        )

        # Frame del logo
        frame_logo = tk.Frame(
            self.window,
            bd=0,
            width=300,
            relief=tk.SOLID,
            padx=10,
            pady=10,
            bg=util.Colors.blacklike,
        )
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame del registro
        frame_form = tk.form = tk.Frame(
            self.window, bd=0, relief=tk.SOLID, bg=util.Colors.greylike
        )
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        frame_form_top = tk.Frame(
            frame_form, height=20, bd=0, relief=tk.SOLID, bg=util.Colors.greylike
        )
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(
            frame_form_top,
            text="Crea tu cuenta",
            font=("Microsoft Phags Pa", 30, BOLD),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            pady=50,
        )
        title.pack(expand=tk.YES, fill=tk.BOTH)

        frame_form_fill = tk.Frame(
            frame_form, height=80, bd=0, relief=tk.SOLID, bg=util.Colors.greylike
        )
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        names_tag = tk.Label(
            frame_form_fill,
            text="Nombres",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        names_tag.pack(fill=tk.X, padx=20, pady=5)
        self.names = ttk.Entry(frame_form_fill, font=("Microsoft Phags Pa", 14))
        self.names.pack(fill=tk.X, padx=20, pady=10)

        lastname_tag = tk.Label(
            frame_form_fill,
            text="Apellidos",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        lastname_tag.pack(fill=tk.X, padx=20, pady=5)
        self.lastnames = ttk.Entry(frame_form_fill, font=("Microsoft Phags Pa", 14))
        self.lastnames.pack(fill=tk.X, padx=20, pady=10)

        user_tag = tk.Label(
            frame_form_fill,
            text="Usuario",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        user_tag.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=("Microsoft Phags Pa", 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        password_tag = tk.Label(
            frame_form_fill,
            text="Escribe una contraseña",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        password_tag.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(
            frame_form_fill, font=("Microsoft Phags Pa", 14), show="*"
        )
        self.password.pack(fill=tk.X, padx=20, pady=10)

        password1_tag = tk.Label(
            frame_form_fill,
            text="Escribe nuevamente la contraseña",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        password1_tag.pack(fill=tk.X, padx=20, pady=5)
        self.password1 = ttk.Entry(
            frame_form_fill, font=("Microsoft Phags Pa", 14), show="*"
        )
        self.password1.pack(fill=tk.X, padx=20, pady=10)

        access_button = tk.Button(
            frame_form_fill,
            text="Crear usuario",
            font=("Microsoft Phags Pa", 15, BOLD),
            bg=util.Colors.pinklike,
            fg=util.Colors.white,
            bd=0,
            command=self.verify_register,
        )
        access_button.pack(fill=tk.X, padx=20, pady=20)

        self.profile_picture = os.path.join(".", "media", "pictures", "fotos_perfil", "foto_perfil0.png")
        self.nivel_privilegio = 2
        self.apps = []
        self.fondo_pantalla = os.path.join(".", "media", "pictures", "fondos_pantalla", "fondo_pantalla0.jpg")

        profile_picture_button = tk.Button(
            frame_form_fill,
            text="Seleccionar foto de perfil",
            font=("Microsoft Phags Pa", 15, BOLD),
            bg=util.Colors.pinklike,
            fg=util.Colors.white,
            bd=0,
            command=self.select_profile,
        )
        profile_picture_button.pack(fill=tk.X, padx=20, pady=20)

        self.window.mainloop()
