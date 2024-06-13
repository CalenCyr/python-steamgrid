import json
import os
import platform
import requests
import vdf
import xmltodict

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
    """Retrieve Steam user names and IDs by parsing config.vdf."""
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
    user_data = config_data.get('InstallConfigStore', {}).get('Software', {}).get('Valve', {}).get('Steam', {}).get('Accounts', {})
    
    for steam_username, data in user_data.items():
        steam_id = data.get('SteamID')
        if steam_username:
            users.append({'username': steam_username, 'steam_id': steam_id})
    
    return users

def get_profile(user_id):
    """Retrieve the Steam profile information for a given user by parsing the localconfig.vdf file."""
    steam_path = get_steam_installation()
    user_data_path = os.path.join(steam_path, "userdata", str(user_id), "config", "localconfig.vdf")

    if not os.path.exists(user_data_path):
        raise FileNotFoundError(f"localconfig.vdf not found at {user_data_path}")

    try:
        with open(user_data_path, 'r', encoding='utf-8') as f:
            user_data = vdf.load(f)
    except Exception as e:
        raise IOError(f"Failed to read localconfig.vdf: {e}")

    profile_data = user_data.get('UserLocalConfigStore', {}).get('friends', {}).get('PersonaName', None)
    
    if not profile_data:
        raise ValueError("Profile data not found in localconfig.vdf")

    return profile_data

def get_installed_games():
    """Retrieve a list of installed Steam games by parsing appmanifest_*.acf files."""
    library_folders = get_library_folders()
    games = []

    for folder in library_folders:
        for file_name in os.listdir(folder):
            if file_name.startswith("appmanifest_") and file_name.endswith(".acf"):
                appmanifest_path = os.path.join(folder, file_name)
                try:
                    with open(appmanifest_path, 'r', encoding='utf-8') as f:
                        game_data = vdf.load(f)
                    app_state = game_data.get('AppState', {})
                    name = app_state.get('name')
                    appid = app_state.get('appid')
                    if name and appid:
                        games.append({'name': name, 'appid': appid})
                except Exception as e:
                    print(f"Failed to read {appmanifest_path}: {e}")
    
    return games

def get_library_folders():
    """Retrieve a list of library folders by parsing libraryfolders.vdf."""
    steam_path = get_steam_installation()
    library_folders_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

    if not os.path.exists(library_folders_path):
        raise FileNotFoundError(f"libraryfolders.vdf not found at {library_folders_path}")

    try:
        with open(library_folders_path, 'r', encoding='utf-8') as f:
            library_data = vdf.load(f)
    except Exception as e:
        raise IOError(f"Failed to read libraryfolders.vdf: {e}")

    library_folders = [os.path.join(steam_path, "steamapps")]
    additional_folders = library_data.get('libraryfolders', {})
    
    for key, value in additional_folders.items():
        if key.isdigit():
            path = value.get('path')
            if path:
                library_folders.append(os.path.join(path, "steamapps"))

    return library_folders

def get_all_games():
    """Retrieve a list of all games by parsing config.vdf."""
    steam_path = get_steam_installation()
    config_path = os.path.join(steam_path, "config", "config.vdf")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.vdf not found at {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = vdf.load(f)
    except Exception as e:
        raise IOError(f"Failed to read config.vdf: {e}")

    games = []
    accounts = config_data.get('InstallConfigStore', {}).get('Software', {}).get('Valve', {}).get('Steam', {}).get('apps', {})
    print(json.dumps(config_data, indent=4))

    for appid, app_data in accounts.items():
        name = app_data.get('name')
        if name:
            games.append({'name': name, 'appid': appid})

    return games

def fetch_and_parse_games_xml(profile_id):
    """
    Fetch the games XML from Steam community profile and parse it to JSON.
    Think about replacing this with Steam API later or as a backup (would likely require dev API key)

    Return data example:
        gamesList
            steamID64 (Steam ID)
            SteamID: (public username)
            games (object)
                game (list)
                    appId (Steam App ID)
                    name (Full name)
                    logo (Main cover art, capsule image likely)
                    hoursLast2Weeks
                    hoursOnRecord
                    statsLink
                    globalStatsLink
    """
    url = f"https://steamcommunity.com/profiles/{profile_id}/games?xml=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error fetching data from Steam: {e}")
    
    try:
        data_dict = xmltodict.parse(response.content)
    except Exception as e:
        raise SystemExit(f"Error parsing XML data: {e}")
    
    json_data = json.dumps(data_dict, indent=4)
    return json_data

def download_grid_image(image_url, grid_directory):
    """Download the specific grid image from URL and save to the users's grid directory
    
    Parameters
    -----------
    image_url: str
        The image URL

    grid_directory: str
        The user's grid directory will the image will be placed

    Returns
    --------
    None
    """

    # TODO - write method outside of this to get the user's /grid/ directory
    # TODO - handle image by basename so it's named as we expect it, along with the right file type (png/jpg)
    # * `<GAME_ID>.png` (main image for cover used per `/grid/` folder examples)
    # * `<GAME_ID>_icon.png`
    # * `<GAME_ID>_hero.png`
    # * `<GAME_ID>_logo.png`

    # Send a GET request to the image URL
    response = requests.get(image_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary write mode
        with open("{grid_directory}/downloaded_image.jpg", "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        print("Image downloaded successfully")
    else:
        print("Failed to download image, status code:", response.status_code)
