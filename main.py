import json
import os
from forms.form_lock_screen import LockScreen
from forms.form_register import Register
from forms.form_desktop import Desktop

USERS_FILE = "users.json"

if __name__ == "__main__":
    # Check if users file exists
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
        
        # If users exist, show lock screen, otherwise remove corrupted file and register
        if users:
            LockScreen()
        else:
            os.remove(USERS_FILE)
            Register()
    else:
        # No users file exists, start registration
        Register()