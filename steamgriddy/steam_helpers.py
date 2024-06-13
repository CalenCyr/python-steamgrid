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

def get_steam_users():
    """Retrieve a list of Steam users by parsing the config.vdf file."""
    steam_path = get_steam_installation()
    config_path = os.path.join(steam_path, "config", "config.vdf")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.vdf not found at {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = vdf.load(f)
    except Exception as e:
        raise IOError(f"Failed to read config.vdf: {e}")

    users = []
    accounts = config_data.get('InstallConfigStore', {}).get('Software', {}).get('Valve', {}).get('Steam', {}).get('Accounts', {})
    
    for user, data in accounts.items():
        users.append(user)
    
    return users
