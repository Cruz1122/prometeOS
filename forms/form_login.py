import json
import os
import bcrypt
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import utilities.generic as util
from forms.form_desktop import Desktop


class Login:
    """
    Login form class that handles user authentication
    """

    def verify_login(self):
        """
        Verify user credentials and create user directory if needed
        """
        user = self.username.get()
        password = self.password.get()

        with open("users.json", "r") as file:
            users = json.load(file)

        if user in users:
            if bcrypt.checkpw(password.encode("utf-8"), users[user]["password"].encode("utf-8")):
                # Create user folder in /users if it doesn't exist
                user_dir = util.get_user_directory(user)
                if not os.path.exists(user_dir):
                    os.makedirs(user_dir)  # Create user folder

                # Create subfolders if they don't exist
                if not os.path.exists(os.path.join(user_dir, "music")):
                    os.makedirs(os.path.join(user_dir, "music"), exist_ok=True)
                if not os.path.exists(os.path.join(user_dir, "media")):
                    os.makedirs(os.path.join(user_dir, "media"), exist_ok=True)
                if not os.path.exists(os.path.join(user_dir, "documents")):
                    os.makedirs(os.path.join(user_dir, "documents"), exist_ok=True)

                self.window.destroy()
                Desktop(users[user])
                return

        messagebox.showerror("Error", "Incorrect username or password")

    def __init__(self):
        """
        Initialize the login form interface
        """
        self.window = tk.Tk()
        self.window.title("PrometeOS - Login")
        self.window.geometry("800x500")
        self.window.config(bg=util.Colors.white)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap(util.get_icon_path("logo.ico"))
        util.center_window(self.window, 800, 500)

        logo = util.load_image(util.get_image_path("logo.png"), (200, 200))

        # Logo frame
        logo_frame = tk.Frame(self.window, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg=util.Colors.blacklike)
        logo_frame.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(logo_frame, image=logo, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Login form frame
        form_frame = tk.Frame(self.window, bd=0, relief=tk.SOLID, bg=util.Colors.greylike)
        form_frame.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        form_frame_top = tk.Frame(form_frame, height=50, bd=0, relief=tk.SOLID, bg=util.Colors.greylike)
        form_frame_top.pack(side="top", fill=tk.X)
        title = tk.Label(form_frame_top, text="Login", font=("Microsoft Phags Pa", 30, BOLD), bg=util.Colors.greylike, fg=util.Colors.white, pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        form_frame_fill = tk.Frame(form_frame, height=50, bd=0, relief=tk.SOLID, bg=util.Colors.greylike)
        form_frame_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        user_tag = tk.Label(form_frame_fill, text="Username", font=("Microsoft Phags Pa", 14), bg=util.Colors.greylike, fg=util.Colors.white, anchor="w")
        user_tag.pack(fill=tk.X, padx=20, pady=5)
        self.username = ttk.Entry(form_frame_fill, font=("Microsoft Phags Pa", 14))
        self.username.pack(fill=tk.X, padx=20, pady=10)

        password_tag = tk.Label(form_frame_fill, text="Password", font=("Microsoft Phags Pa", 14), bg=util.Colors.greylike, fg=util.Colors.white, anchor="w")
        password_tag.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(form_frame_fill, font=("Microsoft Phags Pa", 14), show="*")
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        access_button = tk.Button(form_frame_fill, text="Login", font=("Microsoft Phags Pa", 15, BOLD), bg=util.Colors.pinklike, fg=util.Colors.white, bd=0, command=self.verify_login) 
        access_button.pack(fill=tk.X, padx=20, pady=20)
        self.window.mainloop()
