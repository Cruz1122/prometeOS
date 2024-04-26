import json
import os
import bcrypt
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import utilities.generic as util
from forms.form_desktop import Escritorio

class Login:

    def verify_login(self):
        user = self.usuario.get()
        password = self.password.get()

        with open("users.json", "r") as file:
            users = json.load(file)

        if user in users:
            if bcrypt.checkpw(password.encode("utf-8"), users[user]["password"].encode("utf-8")):
                user_dir = os.path.join("users", user)
                
                if not os.path.exists(user_dir):
                    os.makedirs(user_dir) 
                if not os.path.exists(os.path.join(user_dir, "music")):
                    os.makedirs(os.path.join(user_dir, "music"), exist_ok=True)
                if not os.path.exists(os.path.join(user_dir, "media")):
                    os.makedirs(os.path.join(user_dir, "media"), exist_ok=True)
                if not os.path.exists(os.path.join(user_dir, "documents")):
                    os.makedirs(os.path.join(user_dir, "documents"), exist_ok=True)

                
                self.window.destroy()
                Escritorio(users[user])
                return

        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PrometeOS - Inicio de sesión")
        self.window.geometry("800x500")
        self.window.config(bg=util.Colors.white)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap("./media/icons/logo.ico")
        util.center_window(self.window, 800, 500)

        logo = util.load_image("./media/pictures/logo.png", (200, 200))

        # Frame del logo
        frame_logo = tk.Frame(self.window, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg=util.Colors.blacklike)
        frame_logo.pack(side= "left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame del inicio de sesión
        frame_form = tk.form = tk.Frame(self.window, bd=0, relief=tk.SOLID, bg=util.Colors.greylike)
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        frame_form_top = tk.Frame(frame_form, height= 50, bd=0, relief=tk.SOLID, bg=util.Colors.greylike)
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesión", font=("Microsoft Phags Pa", 30, BOLD), bg=util.Colors.greylike, fg=util.Colors.white, pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg=util.Colors.greylike)
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        user_tag = tk.Label(frame_form_fill, text="Usuario", font=("Microsoft Phags Pa", 14), bg=util.Colors.greylike, fg=util.Colors.white, anchor ="w")
        user_tag.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=("Microsoft Phags Pa", 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        password_tag = tk.Label(frame_form_fill, text="Contraseña", font=("Microsoft Phags Pa", 14), bg=util.Colors.greylike, fg=util.Colors.white, anchor ="w")
        password_tag.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=("Microsoft Phags Pa", 14), show="*")
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        access_button = tk.Button(frame_form_fill, text="Acceder", font=("Microsoft Phags Pa", 15, BOLD), bg=util.Colors.pinklike, fg=util.Colors.white, bd=0, command= self.verify_login) 
        access_button.pack(fill=tk.X, padx=20, pady=20)
        self.window.mainloop()
