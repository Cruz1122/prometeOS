import json
import os
from forms.form_lock_screen import LockScreen
from forms.form_register import Register
from forms.form_desktop import Escritorio

Escritorio(
    {
        "username": "Spot",
        "password": "$2b$12$pMBSveNvfQ.C64pBCvNiSesBxU4L/NlENxGUcfRlhCjyvtvyvDW8.",
        "names": "Camilo",
        "lastnames": "Cruz",
        "profile_picture": "C:/Users/juanc/OneDrive/Documentos/2024-1/Sistemas Operativos/Proyecto/media/pictures/fotos_perfil/foto_perfil0.png",
        "wallpaper": "C:/Users/juanc/OneDrive/Documentos/2024-1/Sistemas Operativos/Proyecto/media/pictures/fondos_pantalla/fondo_pantalla0.jpg",
        "privilege": 2,
        "apps": [],
    }
)

"""
if __name__ == "__main__":

    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
        if users:
            LockScreen()
        else:
            os.remove("users.json")
            Register()
    else:
        Register()
"""
