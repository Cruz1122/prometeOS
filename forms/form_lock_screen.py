import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter.font import BOLD
import utilities.generic as util
from forms.form_login import Login
from forms.form_register import Register


class LockScreen:
    """
    Lock screen class that provides options to login or register
    """
    
    def __init__(self):
        """
        Initialize the lock screen interface
        """
        def register():
            """Open registration form"""
            self.window.destroy()
            Register()

        def login():
            """Open login form"""
            self.window.destroy()
            Login()

        self.window = tk.Tk()
        self.window.title("PrometeOS")
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
            height=300,
            relief=tk.SOLID,
            padx=10,
            pady=10,
            bg=util.Colors.blacklike,
        )
        logo_frame.pack(side="top", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(logo_frame, image=logo, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Form frame
        form_frame = tk.Frame(
            self.window, bd=0, height=500, relief=tk.SOLID, bg=util.Colors.greylike
        )
        form_frame.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Inner frame to center the buttons
        buttons_frame = tk.Frame(form_frame, relief=tk.SOLID, bg=util.Colors.greylike)
        buttons_frame.pack(expand=tk.YES)

        # Login button
        login_button = tk.Button(
            buttons_frame,
            text="Login",
            font=("Microsoft Phags Pa", 16, BOLD),
            width=40,
            bg=util.Colors.pinklike,
            fg='white',
            bd=0,
            command=login,
        )
        login_button.pack(pady=10)  # Internal padding

        # Register button
        register_button = tk.Button(
            buttons_frame,
            text="Create account",
            font=("Microsoft Phags Pa", 16, BOLD),
            width=40,
            bg=util.Colors.redlike,
            fg='white',
            bd=0,
            command=register,
        )
        register_button.pack(pady=10)

        self.window.mainloop()
