import json
import os
from forms.form_lock_screen import LockScreen
from forms.form_register import Register
from forms.form_desktop import Escritorio

Escritorio(
    {
        "username": "Spot",
        "password": "$2b$12$CSV2p2wu54WdpYh5IwE0ZeZX/PP8.mr.FJEPqJ20Wr8HutWhEESAW",
        "names": "Camilo",
        "lastnames": "Cruz",
        "profile_picture": ".\\media\\pictures\\fotos_perfil\\foto_perfil0.png",
        "wallpaper": ".\\media\\pictures\\fondos_pantalla\\fondo_pantalla0.jpg",
        "privilege": 3,
        "apps": ["lizard", "calculadora", "reproductor_audio", "explorador_archivos", "monitor_recursos"]
    }
)


"""if __name__ == "__main__":

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
        Register()"""
