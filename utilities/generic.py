import bcrypt
import PIL
from PIL import ImageTk, Image


class Colors:
    pinklike = "#e99b9b"
    blacklike = "#302939"
    white = "#ffffff"
    redlike = "#e07171"
    greylike = "#493e57"

def load_image(path, size):
    return ImageTk.PhotoImage(
        Image.open(path).resize(size, PIL.Image.Resampling.LANCZOS)
    )

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    return window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def code_password(password):
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    return hashed.decode("utf-8")
