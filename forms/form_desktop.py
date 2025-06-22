import datetime
import os
import subprocess
import tkinter as tk
from tkinter.font import BOLD
import utilities.generic as util
import threading


class Desktop:
    """
    Desktop class that manages the main desktop interface
    Handles wallpaper, applications, taskbar, and system menu
    """
    
    def __init__(self, user):
        """
        Initialize the desktop interface
        
        Args:
            user (dict): User information dictionary
        """
        self.window = tk.Tk()
        self.window.title("Desktop of " + user["names"])
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight() - 80

        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.config(bg=util.Colors.pinklike)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap(util.get_icon_path("logo.ico"))

        wallpaper = util.load_image(user["wallpaper"], (w, h))
        apps_buttons = []

        label = tk.Label(self.window, image=wallpaper, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.lower()

        def change_wallpaper():
            """Open file dialog to select a new wallpaper"""
            path = tk.filedialog.askopenfilename(
                initialdir=util.get_wallpaper_path(""),
                title="Select an image",
                filetypes=[("JPG Files", "*.jpg"), ("PNG Files", "*.png")],
            )
            if path:
                wallpaper = util.load_image(path, (w, h))
                label.config(image=wallpaper)
                label.image = wallpaper

        def close_session():
            """Close the current session"""
            self.window.destroy()

        self.settings_menu = tk.Menu(self.window, tearoff=0)
        self.settings_menu.add_command(
            label="Change wallpaper",
            command=change_wallpaper,
        )
        self.settings_menu.add_command(
            label="Log out",
            command=close_session,
        )

        def show_settings_menu():
            """Display the settings menu at the correct position"""
            x = settings_button.winfo_rootx()
            y = settings_button.winfo_rooty() - settings_button.winfo_height() - 27
            self.settings_menu.tk_popup(x, y)

        self.apps_frame = tk.Frame(
            self.window,
            bg=util.Colors.blacklike,
            bd=5,
            relief="raised",
            width=400,
            height=400,
        )
        self.apps_frame.place(relx=0.5, rely=0.5, anchor="center", x=0, y=115)
        self.apps_frame.grid_propagate(
            False
        )  # Prevent the frame from changing size to fit its contents
        self.apps_frame.lower()

        self.deployed = None
        self.button_row = 0
        self.button_column = 0

        def execute_app(directory, name):
            """Execute an application in a separate thread"""
            def run_script():
                subprocess.run(
                    [
                        "python",
                        os.path.join(directory, name + ".py"),
                        util.get_user_directory(str(user["username"])),
                        os.path.join(str(user["privilege"])),
                    ]
                )

            thread = threading.Thread(target=run_script)
            thread.setDaemon(True)
            thread.start()

        def create_app_button(app_name):
            """Create a button for an application"""
            app_name = app_name.lower()
            icon_app = tk.PhotoImage(file=util.get_app_icon_png_path(app_name))

            apps_buttons.append(
                tk.Button(
                    self.apps_frame,
                    image=icon_app,
                    command=lambda app_name=app_name: execute_app(
                        os.path.join(util.get_apps_directory(), app_name), app_name
                    ),
                    bg=util.Colors.greylike,
                    activebackground=util.Colors.greylike,
                    fg="white",
                    bd=0,
                    padx=10,
                    highlightthickness=0,
                    width=100,
                    height=100,
                )
            )

            apps_buttons[-1].grid(
                row=self.button_row, column=self.button_column, padx=15, pady=10
            )
            apps_buttons[-1].image = icon_app

            self.button_column += 1

            if self.button_column == 3:
                self.button_column = 0
                self.button_row += 1

        if len(user["apps"]) > 0:  # If the user has applications
            for app in user["apps"]:
                if app.lower() in os.listdir(util.get_apps_directory()):
                    create_app_button(app)

        def deploy_apps():
            """Toggle the applications panel visibility"""
            if self.deployed is None:
                self.deployed = False

            if self.deployed:
                self.apps_frame.lower()
                self.deployed = False
            else:
                self.apps_frame.lift()
                self.deployed = True

        taskbar_frame = tk.Frame(self.window, bg=util.Colors.greylike, height=40)
        taskbar_frame.pack(side="bottom", fill="x")

        taskbar_frame.columnconfigure(0, weight=1)
        taskbar_frame.columnconfigure(1, weight=1)
        taskbar_frame.columnconfigure(2, weight=1)
        taskbar_frame.lift()

        icon_settings = tk.PhotoImage(
            file=util.get_app_icon_png_path("configuracion")
        ).subsample(9, 9)
        settings_button = tk.Button(
            taskbar_frame,
            image=icon_settings,
            command=show_settings_menu,
            bg=util.Colors.greylike,
            activebackground=util.Colors.greylike,
            fg="white",
            bd=0,
            highlightthickness=0,
            width=30,
            height=30,
        )
        settings_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        icon_apps = tk.PhotoImage(
            file=util.get_image_path("logo.png")
        ).subsample(8, 8)
        apps_button = tk.Button(
            taskbar_frame,
            image=icon_apps,
            command=deploy_apps,
            bg=util.Colors.greylike,
            activebackground=util.Colors.greylike,
            fg="white",
            width=30,
            height=30,
        )
        apps_button.grid(row=0, column=1, pady=10)

        self.clock_label = tk.Label(
            taskbar_frame, text="", bg=util.Colors.greylike, fg="white"
        )
        self.clock_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        self.clock_thread = threading.Thread(target=self.update_clock, name="Clock")
        self.clock_thread.setDaemon(True)  # Set thread as daemon
        self.clock_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.mainloop()

    def update_clock(self):
        """Update the clock display every second"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.window.after(1000, self.update_clock)  # Call the function every second
