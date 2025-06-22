# PrometeOS

A Python-based operating system simulation built with Tkinter that provides a complete desktop environment with various applications, user management, and system utilities.

## Features

### Core System
- **Multi-User System**: Registration and login with password hashing using bcrypt
- **Desktop Environment**: Full-screen desktop with customizable wallpapers
- **Taskbar**: System clock, application launcher, and settings menu
- **File System**: User-specific directories for documents, music, and media
- **Privilege System**: Different access levels for users

### Applications
- **Notepad**: Text editor with file operations
- **Scientific Calculator**: Advanced calculator with trigonometric functions
- **File Manager**: Complete file and directory management
- **Image Viewer**: View images and videos using system default apps
- **Audio Player**: Music player with playlist management
- **Web Browser**: Opens default system browser
- **Resource Monitor**: Process management and system monitoring
- **Lizard Game**: Chrome Dino-style game with sound effects

## Technologies Used

### Core Technologies
- **Python 3.11+**: Main programming language
- **Tkinter**: GUI framework for desktop interface
- **Pygame**: Game engine for Lizard game
- **Pillow (PIL)**: Image processing and manipulation
- **bcrypt**: Password hashing and security
- **psutil**: System resource monitoring

### Libraries and Dependencies
```bash
bcrypt==4.1.2      # Password hashing
Pillow==10.1.0     # Image processing
pygame==2.5.2       # Game development
psutil==5.9.6       # System monitoring
```

## Project Architecture

```
proyecto/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── users.json                # User data storage
├── .gitignore               # Git ignore rules
│
├── forms/                   # UI Forms and Windows
│   ├── form_desktop.py     # Main desktop interface
│   ├── form_login.py       # User authentication
│   ├── form_register.py    # User registration
│   └── form_lock_screen.py # System lock screen
│
├── apps/                    # Applications
│   ├── bloc_notas/         # Notepad application
│   ├── calculadora/        # Scientific calculator
│   ├── explorador_archivos/ # File manager
│   ├── visor_imagenes/     # Image viewer
│   ├── reproductor_audio/  # Audio player
│   ├── navegador/          # Web browser
│   ├── monitor_recursos/   # Resource monitor
│   ├── lizard/             # Lizard game
│   └── configuracion/      # Settings (icon only)
│
├── utilities/              # Utility functions
│   └── generic.py         # Common utilities and helpers
│
└── media/                 # Media assets
    ├── icons/             # System and app icons
    └── pictures/          # Images and wallpapers
```

## System Flow

### 1. Application Startup (`main.py`)
```python
# Check if users exist
if os.path.exists(USERS_FILE):
    # Load existing users
    # Show lock screen if users exist
else:
    # Start registration process
```

### 2. User Registration (`forms/form_register.py`)
- Collect user information (name, username, password)
- Hash password using bcrypt
- Create user directory structure
- Save user data to `users.json`
- Redirect to login

### 3. User Authentication (`forms/form_login.py`)
- Validate username and password
- Create user directories if they don't exist
- Launch desktop environment

### 4. Desktop Environment (`forms/form_desktop.py`)
- Load user wallpaper and preferences
- Display application grid
- Initialize taskbar with clock
- Handle application execution

### 5. Application Execution
- Applications run in separate threads
- Each app receives user directory and privilege level
- Apps can access system utilities through `utilities.generic`

## Code Architecture

### Core Classes

#### Desktop (`forms/form_desktop.py`)
```python
class Desktop:
    """Main desktop interface manager"""
    
    def __init__(self, user):
        # Initialize desktop window
        # Load user preferences
        # Create application grid
        # Setup taskbar and clock
```

#### User Management
```python
# Registration (form_register.py)
users[username] = {
    "username": username,
    "password": util.hash_password(password),
    "names": names,
    "lastnames": lastnames,
    "profile_picture": profile_picture,
    "wallpaper": wallpaper,
    "privilege": privilege_level,
    "apps": available_apps
}
```

### Utility System (`utilities/generic.py`)

#### Path Management
```python
def get_app_icon_png_path(app_name):
    """Get application icon path"""
    
def get_user_directory(username):
    """Get user's home directory"""
    
def get_wallpaper_path(image_name):
    """Get wallpaper image path"""
```

#### Security
```python
def hash_password(password):
    """Hash password using bcrypt"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode("utf-8")
```

### Application Framework

Each application follows this structure:
```python
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_dir)

import utilities.generic as util

class ApplicationName:
    def __init__(self, root):
        # Initialize application
        # Setup UI components
        # Handle user interactions
```

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd proyecto
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the system**
```bash
python main.py
```

### First Run
- System will prompt for user registration
- Create your first user account
- Set up your profile and preferences

## Application Details

### Notepad (`apps/bloc_notas/bloc_notas.py`)
- **Features**: Text editing, file operations, undo/redo
- **File Support**: .txt files in user's documents folder
- **Operations**: New, open, save, save as

### Calculator (`apps/calculadora/calculadora.py`)
- **Features**: Scientific calculator with GUI
- **Functions**: Basic arithmetic, trigonometric, square root
- **Interface**: Button-based input with display

### File Manager (`apps/explorador_archivos/explorador_archivos.py`)
- **Features**: File and directory management
- **Operations**: Copy, paste, delete, rename, create
- **Security**: Restricted to user directory

### Audio Player (`apps/reproductor_audio/reproductor_audio.py`)
- **Features**: Music playback with playlist
- **Format Support**: MP3 files
- **Controls**: Play, pause, next, previous, remove

### Resource Monitor (`apps/monitor_recursos/monitor_recursos.py`)
- **Features**: Process monitoring and management
- **Operations**: View running processes, terminate processes
- **Security**: Only shows Python processes

### Lizard Game (`apps/lizard/lizard.py`)
- **Features**: Chrome Dino-style game
- **Controls**: Space/Up to jump, Down to duck
- **Assets**: Sprites, sounds, animations

## Security Features

### Password Security
- Passwords hashed using bcrypt
- Salt generation for each password
- Secure password verification

### File System Security
- Users restricted to their own directories
- Privilege-based access control
- Path validation to prevent directory traversal

### Process Security
- Only Python processes visible in resource monitor
- Process termination limited to user's own processes

## UI/UX Design

### Color Scheme
```python
class Colors:
    pinklike = "#e99b9b"    # Primary accent
    blacklike = "#302939"   # Dark background
    white = "#ffffff"       # Text color
    redlike = "#e07171"     # Error/delete actions
    greylike = "#493e57"    # Secondary background
```

### Layout System
- **Desktop**: Full-screen with wallpaper background
- **Applications**: Grid layout with icons
- **Taskbar**: Fixed bottom bar with clock and controls
- **Windows**: Centered with consistent styling

## Development

### Adding New Applications
1. Create new folder in `apps/`
2. Add `icon.png` for the application
3. Follow the application template structure
4. Update user privileges to include the new app

### Customization
- **Colors**: Modify `utilities/generic.py` Colors class
- **Wallpapers**: Add images to `media/pictures/wallpapers/`
- **Icons**: Update application icons in respective folders

### Testing
- Test user registration and login
- Verify application functionality
- Check file system operations
- Test privilege system

## Code Quality

### Documentation
- All functions have docstrings
- Class documentation with purpose and usage
- Parameter and return value documentation
- Inline comments for complex logic

### Code Style
- PEP 8 compliance
- Consistent naming conventions
- Modular design with separation of concerns
- Error handling and validation

### Performance
- Threading for application execution
- Efficient file operations
- Memory-conscious image loading
- Responsive UI updates

## Contributing

This is an academic project for Operating Systems course. For educational contributions:

1. Follow existing code structure
2. Maintain documentation standards
3. Test thoroughly before submitting
4. Use consistent naming conventions

## License

This project is for educational purposes as part of an Operating Systems course.

## Known Issues

- Limited to Python processes in resource monitor
- Audio player supports only MP3 format
- Image viewer uses system default applications
- Web browser opens external browser

## Future Enhancements

- Multi-language support
- Additional applications (email, calendar, etc.)
- Network functionality
- Advanced security features
- Plugin system for applications
- System settings and configuration
- Backup and restore functionality

---

**PrometeOS** - A complete operating system simulation built with Python and Tkinter.
