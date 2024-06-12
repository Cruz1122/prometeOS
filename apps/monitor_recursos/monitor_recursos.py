import tkinter as tk
from tkinter import messagebox
import psutil
import os
import psutil
import ctypes
import ctypes.wintypes


def get_window_title(pid):
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(
        ctypes.wintypes.BOOL,
        ctypes.wintypes.HWND,
        ctypes.POINTER(ctypes.wintypes.LPARAM),
    )
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    titles = []

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            pid_of_window = ctypes.wintypes.DWORD()
            GetWindowThreadProcessId(hwnd, ctypes.byref(pid_of_window))
            if pid_of_window.value == pid:
                titles.append(buff.value)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles[0] if titles else None


class MonitorRecursos:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Recursos")
        self.root.iconbitmap("apps/monitor_recursos/icon.ico")
        self.root.geometry("1100x600")

        self.process_listbox = tk.Listbox(
            self.root, selectmode=tk.SINGLE, width=80, height=20
        )
        self.process_listbox.pack(pady=20)

        self.refresh_button = tk.Button(
            self.root, text="Refrescar", command=self.update_process_list
        )
        self.refresh_button.pack(pady=5)

        self.terminate_button = tk.Button(
            self.root, text="Terminar Proceso", command=self.terminate_process
        )
        self.terminate_button.pack(pady=5)

        self.update_process_list()

    def update_process_list(self):
        self.process_listbox.delete(0, tk.END)
        for process in psutil.process_iter(["pid"]):
            try:
                if process.name() in ("python", "python.exe"):
                    window_title = get_window_title(process.info["pid"])
                    if window_title and "Escritorio" not in window_title:
                        self.process_listbox.insert(
                            tk.END, f"{process.info['pid']} - {window_title}"
                        )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def terminate_process(self):
        try:
            selected = self.process_listbox.get(self.process_listbox.curselection())
            pid = int(selected.split(" - ")[0])
            p = psutil.Process(pid)
            p.terminate()
            messagebox.showinfo("Éxito", f"Proceso {pid} terminado.")
            self.update_process_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorRecursos(root)
    root.mainloop()
