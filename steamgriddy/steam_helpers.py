import os
import platform

def get_steam_installation():
    # Check if the STEAM environment variable is set
    steam_path = os.getenv("STEAM")
    if steam_path:
        return steam_path
    
    # Get the home directory
    home = os.path.expanduser("~")
    if not home:
        raise EnvironmentError("HOME environment variable not set")

    # List of default installation paths
    default_installations = [
        os.path.join(home, ".steam", "steam"),
        os.path.join(home, ".local", "share", "Steam"),
        os.path.join(home, "Library", "Application Support", "Steam"),
        "C:\\Program Files (x86)\\Steam"
    ]

    # Check each default path
    for path in default_installations:
        if os.path.exists(path):
            return path

    # If no installation path is found
    raise FileNotFoundError("Could not find Steam installation")

