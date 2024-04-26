import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter.font import BOLD
import utilities.generic as util
from forms.form_login import Login
from forms.form_register import Register

class LockScreen:
    def __init__(self):

        def register():
            self.window.destroy()
            Register()

        def login():
            self.window.destroy()
            Login()

        self.window = tk.Tk()
        self.window.title("PrometeOS")
        self.window.geometry("800x800")
        self.window.config(bg=util.Colors.white)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap("./media/icons/logo.ico")
        util.center_window(self.window, 800, 800)

        logo = util.load_image("./media/pictures/logo.png", (200, 200))

        # Frame del logo
        frame_logo = tk.Frame(
            self.window,
            bd=0,
            height=300,
            relief=tk.SOLID,
            padx=10,
            pady=10,
            bg=util.Colors.blacklike,
        )
        frame_logo.pack(side="top", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame del registro
        frame_form = tk.form = tk.Frame(
            self.window, bd=0, height=500, relief=tk.SOLID, bg=util.Colors.greylike
        )
        frame_form.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Inner frame to center the buttons
        frame_buttons = tk.Frame(frame_form, relief=tk.SOLID, bg=util.Colors.greylike)
        frame_buttons.pack(expand=tk.YES)

        # Login button
        login_button = tk.Button(
            frame_buttons,
            text="Iniciar sesión",
            font=("Microsoft Phags Pa", 16, BOLD),
            width= 40,
            bg=util.Colors.pinklike,
            fg='white',
            bd=0,
            command=login,
        )
        login_button.pack(pady=10)  # Padding interno

        # Register button
        register_button = tk.Button(
            frame_buttons,
            text="Crear cuenta",
            font=("Microsoft Phags Pa", 16, BOLD),
            width=40,
            bg=util.Colors.redlike,
            fg='white',
            bd=0,
            command=register,
        )
        register_button.pack(pady=10)

        self.window.mainloop()
