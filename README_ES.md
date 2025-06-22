# PrometeOS

Una simulación de sistema operativo basada en Python construida con Tkinter que proporciona un entorno de escritorio completo con diversas aplicaciones, gestión de usuarios y utilidades del sistema.

## Características

### Sistema Principal
- **Sistema Multi-Usuario**: Registro e inicio de sesión con hash de contraseñas usando bcrypt
- **Entorno de Escritorio**: Escritorio de pantalla completa con fondos personalizables
- **Barra de Tareas**: Reloj del sistema, lanzador de aplicaciones y menú de configuración
- **Sistema de Archivos**: Directorios específicos de usuario para documentos, música y medios
- **Sistema de Privilegios**: Diferentes niveles de acceso para usuarios

### Aplicaciones
- **Bloc de Notas**: Editor de texto con operaciones de archivo
- **Calculadora Científica**: Calculadora avanzada con funciones trigonométricas
- **Administrador de Archivos**: Gestión completa de archivos y directorios
- **Visor de Imágenes**: Ver imágenes y videos usando aplicaciones del sistema
- **Reproductor de Audio**: Reproductor de música con gestión de listas de reproducción
- **Navegador Web**: Abre el navegador predeterminado del sistema
- **Monitor de Recursos**: Gestión de procesos y monitoreo del sistema
- **Juego Lizard**: Juego estilo Chrome Dino con efectos de sonido

## Tecnologías Utilizadas

### Tecnologías Principales
- **Python 3.11+**: Lenguaje de programación principal
- **Tkinter**: Framework GUI para la interfaz de escritorio
- **Pygame**: Motor de juegos para el juego Lizard
- **Pillow (PIL)**: Procesamiento y manipulación de imágenes
- **bcrypt**: Hash de contraseñas y seguridad
- **psutil**: Monitoreo de recursos del sistema

### Librerías y Dependencias
```bash
bcrypt==4.1.2      # Hash de contraseñas
Pillow==10.1.0     # Procesamiento de imágenes
pygame==2.5.2       # Desarrollo de juegos
psutil==5.9.6       # Monitoreo del sistema
```

## Arquitectura del Proyecto

```
proyecto/
├── main.py                    # Punto de entrada de la aplicación
├── requirements.txt           # Dependencias de Python
├── users.json                # Almacenamiento de datos de usuario
├── .gitignore               # Reglas de Git ignore
│
├── forms/                   # Formularios y Ventanas UI
│   ├── form_desktop.py     # Interfaz principal del escritorio
│   ├── form_login.py       # Autenticación de usuario
│   ├── form_register.py    # Registro de usuario
│   └── form_lock_screen.py # Pantalla de bloqueo del sistema
│
├── apps/                    # Aplicaciones
│   ├── bloc_notas/         # Aplicación de bloc de notas
│   ├── calculadora/        # Calculadora científica
│   ├── explorador_archivos/ # Administrador de archivos
│   ├── visor_imagenes/     # Visor de imágenes
│   ├── reproductor_audio/  # Reproductor de audio
│   ├── navegador/          # Navegador web
│   ├── monitor_recursos/   # Monitor de recursos
│   ├── lizard/             # Juego Lizard
│   └── configuracion/      # Configuración (solo icono)
│
├── utilities/              # Funciones de utilidad
│   └── generic.py         # Utilidades y ayudantes comunes
│
└── media/                 # Recursos multimedia
    ├── icons/             # Iconos del sistema y aplicaciones
    └── pictures/          # Imágenes y fondos de pantalla
```

## Flujo del Sistema

### 1. Inicio de la Aplicación (`main.py`)
```python
# Verificar si existen usuarios
if os.path.exists(USERS_FILE):
    # Cargar usuarios existentes
    # Mostrar pantalla de bloqueo si existen usuarios
else:
    # Iniciar proceso de registro
```

### 2. Registro de Usuario (`forms/form_register.py`)
- Recopilar información del usuario (nombre, nombre de usuario, contraseña)
- Hashear contraseña usando bcrypt
- Crear estructura de directorios del usuario
- Guardar datos del usuario en `users.json`
- Redirigir al inicio de sesión

### 3. Autenticación de Usuario (`forms/form_login.py`)
- Validar nombre de usuario y contraseña
- Crear directorios de usuario si no existen
- Lanzar entorno de escritorio

### 4. Entorno de Escritorio (`forms/form_desktop.py`)
- Cargar fondo de pantalla y preferencias del usuario
- Mostrar cuadrícula de aplicaciones
- Inicializar barra de tareas con reloj
- Manejar ejecución de aplicaciones

### 5. Ejecución de Aplicaciones
- Las aplicaciones se ejecutan en hilos separados
- Cada aplicación recibe directorio de usuario y nivel de privilegio
- Las aplicaciones pueden acceder a utilidades del sistema a través de `utilities.generic`

## Arquitectura del Código

### Clases Principales

#### Escritorio (`forms/form_desktop.py`)
```python
class Desktop:
    """Gestor de interfaz principal del escritorio"""
    
    def __init__(self, user):
        # Inicializar ventana del escritorio
        # Cargar preferencias del usuario
        # Crear cuadrícula de aplicaciones
        # Configurar barra de tareas y reloj
```

#### Gestión de Usuarios
```python
# Registro (form_register.py)
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

### Sistema de Utilidades (`utilities/generic.py`)

#### Gestión de Rutas
```python
def get_app_icon_png_path(app_name):
    """Obtener ruta del icono de la aplicación"""
    
def get_user_directory(username):
    """Obtener directorio principal del usuario"""
    
def get_wallpaper_path(image_name):
    """Obtener ruta de la imagen de fondo"""
```

#### Seguridad
```python
def hash_password(password):
    """Hashear contraseña usando bcrypt"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode("utf-8")
```

### Framework de Aplicaciones

Cada aplicación sigue esta estructura:
```python
import sys
import os

# Agregar directorio raíz del proyecto al path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_dir)

import utilities.generic as util

class NombreAplicacion:
    def __init__(self, root):
        # Inicializar aplicación
        # Configurar componentes UI
        # Manejar interacciones del usuario
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.11 o superior
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd proyecto
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar el sistema**
```bash
python main.py
```

### Primera Ejecución
- El sistema solicitará registro de usuario
- Crear tu primera cuenta de usuario
- Configurar tu perfil y preferencias

## Detalles de las Aplicaciones

### Bloc de Notas (`apps/bloc_notas/bloc_notas.py`)
- **Características**: Edición de texto, operaciones de archivo, deshacer/rehacer
- **Soporte de Archivos**: Archivos .txt en la carpeta de documentos del usuario
- **Operaciones**: Nuevo, abrir, guardar, guardar como

### Calculadora (`apps/calculadora/calculadora.py`)
- **Características**: Calculadora científica con interfaz gráfica
- **Funciones**: Aritmética básica, trigonométrica, raíz cuadrada
- **Interfaz**: Entrada basada en botones con pantalla

### Administrador de Archivos (`apps/explorador_archivos/explorador_archivos.py`)
- **Características**: Gestión de archivos y directorios
- **Operaciones**: Copiar, pegar, eliminar, renombrar, crear
- **Seguridad**: Restringido al directorio del usuario

### Reproductor de Audio (`apps/reproductor_audio/reproductor_audio.py`)
- **Características**: Reproducción de música con lista de reproducción
- **Soporte de Formatos**: Archivos MP3
- **Controles**: Reproducir, pausar, siguiente, anterior, eliminar

### Monitor de Recursos (`apps/monitor_recursos/monitor_recursos.py`)
- **Características**: Monitoreo y gestión de procesos
- **Operaciones**: Ver procesos en ejecución, terminar procesos
- **Seguridad**: Solo muestra procesos de Python

### Juego Lizard (`apps/lizard/lizard.py`)
- **Características**: Juego estilo Chrome Dino
- **Controles**: Espacio/Arriba para saltar, Abajo para agacharse
- **Recursos**: Sprites, sonidos, animaciones

## Características de Seguridad

### Seguridad de Contraseñas
- Contraseñas hasheadas usando bcrypt
- Generación de salt para cada contraseña
- Verificación segura de contraseñas

### Seguridad del Sistema de Archivos
- Usuarios restringidos a sus propios directorios
- Control de acceso basado en privilegios
- Validación de rutas para prevenir traversal de directorios

### Seguridad de Procesos
- Solo procesos de Python visibles en el monitor de recursos
- Terminación de procesos limitada a procesos propios del usuario

## Diseño UI/UX

### Esquema de Colores
```python
class Colors:
    pinklike = "#e99b9b"    # Acento primario
    blacklike = "#302939"   # Fondo oscuro
    white = "#ffffff"       # Color de texto
    redlike = "#e07171"     # Acciones de error/eliminar
    greylike = "#493e57"    # Fondo secundario
```

### Sistema de Diseño
- **Escritorio**: Pantalla completa con fondo de pantalla
- **Aplicaciones**: Diseño de cuadrícula con iconos
- **Barra de Tareas**: Barra fija inferior con reloj y controles
- **Ventanas**: Centradas con estilo consistente

## Desarrollo

### Agregar Nuevas Aplicaciones
1. Crear nueva carpeta en `apps/`
2. Agregar `icon.png` para la aplicación
3. Seguir la estructura de plantilla de aplicación
4. Actualizar privilegios de usuario para incluir la nueva aplicación

### Personalización
- **Colores**: Modificar clase Colors en `utilities/generic.py`
- **Fondos de Pantalla**: Agregar imágenes a `media/pictures/wallpapers/`
- **Iconos**: Actualizar iconos de aplicaciones en carpetas respectivas

### Pruebas
- Probar registro e inicio de sesión de usuarios
- Verificar funcionalidad de aplicaciones
- Verificar operaciones del sistema de archivos
- Probar sistema de privilegios

## Calidad del Código

### Documentación
- Todas las funciones tienen docstrings
- Documentación de clases con propósito y uso
- Documentación de parámetros y valores de retorno
- Comentarios en línea para lógica compleja

### Estilo de Código
- Cumplimiento PEP 8
- Convenciones de nomenclatura consistentes
- Diseño modular con separación de responsabilidades
- Manejo de errores y validación

### Rendimiento
- Threading para ejecución de aplicaciones
- Operaciones de archivo eficientes
- Carga de imágenes consciente de memoria
- Actualizaciones de UI responsivas

## Contribución

Este es un proyecto académico para el curso de Sistemas Operativos. Para contribuciones educativas:

1. Seguir la estructura de código existente
2. Mantener estándares de documentación
3. Probar exhaustivamente antes de enviar
4. Usar convenciones de nomenclatura consistentes

## Licencia

Este proyecto es para fines educativos como parte de un curso de Sistemas Operativos.

## Problemas Conocidos

- Limitado a procesos de Python en el monitor de recursos
- Reproductor de audio solo soporta formato MP3
- Visor de imágenes usa aplicaciones predeterminadas del sistema
- Navegador web abre navegador externo

## Mejoras Futuras

- Soporte multi-idioma
- Aplicaciones adicionales (correo, calendario, etc.)
- Funcionalidad de red
- Características de seguridad avanzadas
- Sistema de plugins para aplicaciones
- Configuración y ajustes del sistema
- Funcionalidad de respaldo y restauración

---

**PrometeOS** - Una simulación completa de sistema operativo construida con Python y Tkinter. 