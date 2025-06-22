import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter.font import BOLD
import utilities.generic as util
from forms.form_desktop import Desktop
from forms.form_login import Login


class Register:
    """
    Registration form class that handles new user creation
    """

    def verify_register(self):
        """
        Verify registration data and create new user account
        """
        user = self.username.get()
        password = self.password.get()
        password1 = self.password1.get()
        names = self.names.get()
        lastnames = self.lastnames.get()
        profile_picture = self.profile_picture

        if password != password1:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Check if fields are not empty
        if not user or not password or not names or not lastnames:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if not os.path.exists("users.json"):
            with open("users.json", "w") as file:
                json.dump({}, file)
                self.privilege_level = 3
        with open("users.json", "r") as file:
            users = json.load(file)

        if user in users:
            messagebox.showerror("Error", "User already exists")
            return

        users[user] = {
            "username": user,
            "password": util.hash_password(password),
            "names": names,
            "lastnames": lastnames,
            "profile_picture": profile_picture,
            "wallpaper": self.wallpaper,
            "privilege": self.privilege_level,
            "apps": self.apps,
        }

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        # Create user folder in /users
        user_dir = util.get_user_directory(user)
        print(user_dir)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)  # Create user folder

        # Create subfolders
        os.makedirs(os.path.join(user_dir, "music"), exist_ok=True)
        os.makedirs(os.path.join(user_dir, "media"), exist_ok=True)
        os.makedirs(os.path.join(user_dir, "documents"), exist_ok=True)

        self.window.destroy()
        Login()

    def select_profile(self):
        """
        Open file dialog to select a profile picture
        """
        self.profile_picture = filedialog.askopenfilename(
            initialdir=util.get_profile_image_path(""),
            title="Select a profile picture",
            defaultextension=".png",
        )

    def __init__(self):
        """
        Initialize the registration form interface
        """
        self.window = tk.Tk()
        self.window.title("PrometeOS - Create Account")
        self.window.geometry("800x800")
        self.window.config(bg=util.Colors.white)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap(util.get_icon_path("logo.ico"))
        util.center_window(self.window, 800, 800)

        logo = util.load_image(util.get_image_path("logo.png"), (200, 200))

        # Logo frame
        logo_frame = tk.Frame(
            self.window,
            bd=0,
            width=300,
            relief=tk.SOLID,
            padx=10,
            pady=10,
            bg=util.Colors.blacklike,
        )
        logo_frame.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(logo_frame, image=logo, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Registration form frame
        form_frame = tk.Frame(
            self.window, bd=0, relief=tk.SOLID, bg=util.Colors.greylike
        )
        form_frame.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        form_frame_top = tk.Frame(
            form_frame, height=20, bd=0, relief=tk.SOLID, bg=util.Colors.greylike
        )
        form_frame_top.pack(side="top", fill=tk.X)
        title = tk.Label(
            form_frame_top,
            text="Create your account",
            font=("Microsoft Phags Pa", 30, BOLD),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            pady=50,
        )
        title.pack(expand=tk.YES, fill=tk.BOTH)

        form_frame_fill = tk.Frame(
            form_frame, height=80, bd=0, relief=tk.SOLID, bg=util.Colors.greylike
        )
        form_frame_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        names_tag = tk.Label(
            form_frame_fill,
            text="First Names",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        names_tag.pack(fill=tk.X, padx=20, pady=5)
        self.names = ttk.Entry(form_frame_fill, font=("Microsoft Phags Pa", 14))
        self.names.pack(fill=tk.X, padx=20, pady=10)

        lastname_tag = tk.Label(
            form_frame_fill,
            text="Last Names",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        lastname_tag.pack(fill=tk.X, padx=20, pady=5)
        self.lastnames = ttk.Entry(form_frame_fill, font=("Microsoft Phags Pa", 14))
        self.lastnames.pack(fill=tk.X, padx=20, pady=10)

        user_tag = tk.Label(
            form_frame_fill,
            text="Username",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        user_tag.pack(fill=tk.X, padx=20, pady=5)
        self.username = ttk.Entry(form_frame_fill, font=("Microsoft Phags Pa", 14))
        self.username.pack(fill=tk.X, padx=20, pady=10)

        password_tag = tk.Label(
            form_frame_fill,
            text="Enter a password",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        password_tag.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(
            form_frame_fill, font=("Microsoft Phags Pa", 14), show="*"
        )
        self.password.pack(fill=tk.X, padx=20, pady=10)

        password1_tag = tk.Label(
            form_frame_fill,
            text="Enter password again",
            font=("Microsoft Phags Pa", 14),
            bg=util.Colors.greylike,
            fg=util.Colors.white,
            anchor="w",
        )
        password1_tag.pack(fill=tk.X, padx=20, pady=5)
        self.password1 = ttk.Entry(
            form_frame_fill, font=("Microsoft Phags Pa", 14), show="*"
        )
        self.password1.pack(fill=tk.X, padx=20, pady=10)

        access_button = tk.Button(
            form_frame_fill,
            text="Create user",
            font=("Microsoft Phags Pa", 15, BOLD),
            bg=util.Colors.pinklike,
            fg=util.Colors.white,
            bd=0,
            command=self.verify_register,
        )
        access_button.pack(fill=tk.X, padx=20, pady=20)

        self.profile_picture = util.get_profile_image_path("foto_perfil0.png")
        self.privilege_level = 2
        self.apps = [
            "lizard",
            "calculadora",
            "reproductor_audio",
            "explorador_archivos",
            "monitor_recursos",
            "bloc_notas",
            "visor_imagenes",
            "navegador",
        ]
        self.wallpaper = util.get_wallpaper_path("fondo_pantalla0.jpg")

        profile_picture_button = tk.Button(
            form_frame_fill,
            text="Select profile picture",
            font=("Microsoft Phags Pa", 15, BOLD),
            bg=util.Colors.pinklike,
            fg=util.Colors.white,
            bd=0,
            command=self.select_profile,
        )
        profile_picture_button.pack(fill=tk.X, padx=20, pady=20)

        self.window.mainloop()
