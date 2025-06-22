import tkinter as tk
from tkinter import messagebox
import psutil
import os
import psutil
import ctypes
import ctypes.wintypes
import sys

# Add the project root directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_dir)

import utilities.generic as util


def get_window_title(pid):
    """
    Get the window title for a given process ID
    
    Args:
        pid (int): Process ID to get window title for
        
    Returns:
        str: Window title if found, None otherwise
    """
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


class ResourceMonitor:
    """
    Resource monitor application class that displays and manages running processes
    """
    
    def __init__(self, root):
        """
        Initialize the resource monitor application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Resource Monitor")
        self.root.iconbitmap(util.get_app_icon_path("monitor_recursos", "icon.ico"))
        self.root.geometry("1100x600")
        self.root.config(bg="#302939")

        self.process_listbox = tk.Listbox(
            self.root, selectmode=tk.SINGLE, width=80, height=20, background="#493e57", border=0, fg="white", selectbackground="#e07171", selectforeground="white", font=("microsoftphagspa", 12)
        )
        self.process_listbox.pack(pady=20)

        self.refresh_button = tk.Button(
            self.root, text="Refresh", command=self.update_process_list, bg="#e07171", fg="white", font=("microsoftphagspa", 12)
        )
        self.refresh_button.pack(pady=5)

        self.terminate_button = tk.Button(
            self.root, text="Terminate process", command=self.terminate_process, bg="#e07171", fg="white", font=("microsoftphagspa", 12)
        )
        self.terminate_button.pack(pady=5)

        self.update_process_list()

    def update_process_list(self):
        """Update the list of running processes"""
        self.process_listbox.delete(0, tk.END)
        for process in psutil.process_iter(["pid"]):
            try:
                if process.name() in ("python", "python.exe"):
                    window_title = get_window_title(process.info["pid"])
                    if window_title and "Desktop" not in window_title:
                        self.process_listbox.insert(
                            tk.END, f"{process.info['pid']} - {window_title}"
                        )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def terminate_process(self):
        """Terminate the selected process"""
        try:
            selected = self.process_listbox.get(self.process_listbox.curselection())
            pid = int(selected.split(" - ")[0])
            p = psutil.Process(pid)
            p.terminate()
            messagebox.showinfo("Success", f"Process {pid} terminated.")
            self.update_process_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceMonitor(root)
    root.mainloop()
