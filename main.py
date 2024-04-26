import json
import os
from forms.form_lock_screen import LockScreen
from forms.form_register import Register


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
