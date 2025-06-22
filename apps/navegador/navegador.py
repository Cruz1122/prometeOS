import tkinter as tk
import webbrowser


class WebBrowser:
    """
    Web browser application class that opens the default system browser
    """
    
    def __init__(self):
        """
        Initialize the web browser application and open Google homepage
        """
        try:
            webbrowser.open(
                "http://www.google.com"
            )  # Open Google homepage
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not open the browser: {str(e)}")


if __name__ == "__main__":
    app = WebBrowser()
