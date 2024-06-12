import tkinter as tk
import webbrowser


class Navegador:
    def __init__(self):
        try:
            webbrowser.open(
                "http://www.google.com"
            )  # Abre la página de inicio de Google
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo abrir el navegador: {str(e)}")


if __name__ == "__main__":
    app = Navegador()
