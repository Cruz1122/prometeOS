import datetime
import os
import tkinter as tk
from tkinter.font import BOLD
import utilities.generic as util
import threading


class Escritorio:
    def __init__(self, user):
        self.window = tk.Tk()
        self.window.title("Escritorio de " + user["names"])
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight() - 80

        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.config(bg=util.Colors.pinklike)
        self.window.resizable(width=0, height=0)
        self.window.iconbitmap("./media/icons/logo.ico")

        wallpaper = util.load_image(user["wallpaper"], (w, h))

        label = tk.Label(self.window, image=wallpaper, bg=util.Colors.blacklike)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.lower()

        def change_wallpaper():
            path = tk.filedialog.askopenfilename(
                initialdir=os.path.join("media", "pictures", "fondos_pantalla"),
                title="Selecciona una imagen",
                filetypes=[("Archivos JPG", "*.jpg"), ("Archivos PNG", "*.png")],
            )
            if path:
                wallpaper = util.load_image(path, (w, h))
                label.config(image=wallpaper)
                label.image = wallpaper

        def close_session():
            self.window.destroy()

        self.settings_menu = tk.Menu(self.window, tearoff=0)
        self.settings_menu.add_command(
            label="Cambiar fondo de pantalla",
            command=change_wallpaper, 
        )
        self.settings_menu.add_command(
            label="Cerrar sesión",
            command=close_session,  
        )

        def show_settings_menu():
            x = settings_button.winfo_rootx()  
            y = (settings_button.winfo_rooty() - settings_button.winfo_height() - 27) 
            self.settings_menu.tk_popup(x, y)

        self.apps_frame = tk.Frame(
            self.window, bg=util.Colors.blacklike, bd=5, relief="raised", width=400, height=400
        )
        self.apps_frame.place(
            relx=0.5, rely=0.5, anchor="center", x=0, y=115
        ) 
        self.apps_frame.lower()  
        self.deployed = None

        def deploy_apps():
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
            file=os.path.join("apps", "configuracion", "settings.png")
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
            file=os.path.join("media", "pictures", "logo.png")
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

        self.clock_thread = threading.Thread(target=self.update_clock, name="Reloj")
        self.clock_thread.setDaemon(True)  # Establece el hilo como demonio
        self.clock_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

        self.window.mainloop()

    def update_clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.window.after(1000, self.update_clock)  # Llama a la función cada segundo
