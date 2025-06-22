import bcrypt
import PIL
import os
from PIL import ImageTk, Image


class Colors:
    """Color constants used throughout the application"""
    pinklike = "#e99b9b"
    blacklike = "#302939"
    white = "#ffffff"
    redlike = "#e07171"
    greylike = "#493e57"


def get_icon_path(icon_name):
    """
    Get the absolute path of an icon based on the project directory
    
    Args:
        icon_name (str): Name of the icon file
        
    Returns:
        str: Absolute path to the icon file
    """
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to reach the project directory
    project_dir = os.path.dirname(current_dir)
    # Build the path to the icon
    return os.path.join(project_dir, "media", "icons", icon_name)


def get_app_icon_path(app_name, icon_name):
    """
    Get the absolute path of an application icon
    
    Args:
        app_name (str): Name of the application
        icon_name (str): Name of the icon file
        
    Returns:
        str: Absolute path to the application icon
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "apps", app_name, icon_name)


def get_image_path(image_name):
    """
    Get the absolute path of an image in media/pictures
    
    Args:
        image_name (str): Name of the image file
        
    Returns:
        str: Absolute path to the image file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "media", "pictures", image_name)


def get_profile_image_path(image_name):
    """
    Get the absolute path of a profile image
    
    Args:
        image_name (str): Name of the profile image file
        
    Returns:
        str: Absolute path to the profile image
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "media", "pictures", "profile_photos", image_name)


def get_wallpaper_path(image_name):
    """
    Get the absolute path of a wallpaper image
    
    Args:
        image_name (str): Name of the wallpaper file
        
    Returns:
        str: Absolute path to the wallpaper
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "media", "pictures", "wallpapers", image_name)


def get_apps_directory():
    """
    Get the absolute path of the applications directory
    
    Returns:
        str: Absolute path to the apps directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "apps")


def get_users_directory():
    """
    Get the absolute path of the users directory
    
    Returns:
        str: Absolute path to the users directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "..", "users")


def get_user_directory(username):
    """
    Get the absolute path of a specific user's directory
    
    Args:
        username (str): Username
        
    Returns:
        str: Absolute path to the user's directory
    """
    return os.path.join(get_users_directory(), username)


def get_app_icon_png_path(app_name):
    """
    Get the absolute path of a PNG icon for an application
    
    Args:
        app_name (str): Name of the application
        
    Returns:
        str: Absolute path to the application's PNG icon
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "apps", app_name, "icon.png")


def get_app_asset_path(app_name, asset_type, asset_name):
    """
    Get the absolute path of an application asset
    
    Args:
        app_name (str): Name of the application
        asset_type (str): Type of asset (e.g., 'Lizard', 'Cactus', 'Bird')
        asset_name (str): Name of the asset file
        
    Returns:
        str: Absolute path to the application asset
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "apps", app_name, "Assets", asset_type, asset_name)


def get_app_sound_path(app_name, sound_name):
    """
    Get the absolute path of an application sound file
    
    Args:
        app_name (str): Name of the application
        sound_name (str): Name of the sound file
        
    Returns:
        str: Absolute path to the application sound
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    return os.path.join(project_dir, "apps", app_name, "Sounds", sound_name)


def load_image(path, size):
    """
    Load and resize an image for use in tkinter
    
    Args:
        path (str): Path to the image file
        size (tuple): Desired size as (width, height)
        
    Returns:
        ImageTk.PhotoImage: Resized image ready for tkinter
    """
    return ImageTk.PhotoImage(
        Image.open(path).resize(size, PIL.Image.Resampling.LANCZOS)
    )


def center_window(window, width, height):
    """
    Center a window on the screen
    
    Args:
        window: Tkinter window object
        width (int): Window width
        height (int): Window height
        
    Returns:
        str: Geometry string for the centered window
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    return window.geometry('%dx%d+%d+%d' % (width, height, x, y))


def hash_password(password):
    """
    Hash a password using bcrypt
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)

    return hashed.decode("utf-8")
