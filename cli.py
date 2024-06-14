#!/bin/python3

import argparse
import os
import json
import time

from steamgriddy import http
from steamgriddy import ocr
from steamgriddy import SteamGridDB
from steamgriddy import steam_helpers
from steamgriddy import enums

if __name__ == '__main__':
    aparser = argparse.ArgumentParser(
        description="SteamGriddy utility",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog,max_help_position=80,width=100)
    )
    aparser.add_argument('-o', '--only-missing', 
            action='store_true',
            help="Update capsule cover art only if missing."
    )
    aparser.add_argument('-su', '--steam-user', 
            action='store',
            help="Required only if more than one user exist on your system."
    )
    aparser.add_argument('-a', '--api-key',
            action='store',
            help="Your SteamGridDB API KEY (if not stored in ~/.config/steamgriddy)"
    )
    args = aparser.parse_args()

    # Init
    sgdb = SteamGridDB(args.api_key)

    # Get games in users library to interate through
    users = steam_helpers.get_steam_users()
    if not args.steam_user:
        if len(users) > 1:
            exit("Multiple Steam users found on this system, please set --steam-user <NAME>")
        else:
            user_details = users[0]
    else:
        user_details = steam_helpers.get_steam_user_details(args.steam_user)
    if not user_details:
        exit("Failed to find Steam user details!")
    user_id = user_details['username']
    steam_id = user_details['steam_id']
    profile_name = user_details['steam_profile_name']
    if not profile_name:
        exit("Could not fetch profile name!")

    # Get library folders
    print("Attempting to get library folders from VDF")
    steam_library_folders = steam_helpers.get_library_folders()
    if not steam_library_folders:
        exit("Failed to find library folders!")

    steam_librarycache_dir = steam_helpers.get_librarycache_folder()
    steam_grid_dir = steam_helpers.get_grid_folder(steam_id, profile_name)

    print(f"Steam libcache dir: {steam_librarycache_dir}")
    print(f"Steam grid dir: {steam_grid_dir}")

    # Parse games from profile
    # In the future, see if using the Steam API is more future proof
    #   "appID": "233840",
    #   "name": "Worms Clan Wars",
    #   "logo": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/233840/capsule_184x69.jpg?t=1655730300",
    #   "storeLink": "https://steamcommunity.com/app/233840",
    #   "hoursOnRecord": "0.4",
    #   "statsLink": "https://steamcommunity.com/id/ProfessorKaos64/stats/WormsClanWars",
    #   "globalStatsLink": "https://steamcommunity.com/stats/WormsClanWars/achievements/"

    print(f"Fetching {user_id}'s Steam games")
    games = steam_helpers.fetch_and_parse_games_xml(steam_id)

    count = 0
    total_games = len(games)
    if not games:
        exit("Error fetching games!")
    sorted_games = sorted(games, key=lambda item: item['name'], reverse=False)
    for this_game in sorted_games:
        count += 1
        game_appid = this_game["appID"]
        game_name = this_game["name"]
        game_logo = this_game.get("logo", "")

        # TESTING ONLY
        #if game_name != "A Virus Named TOM":
        #    print(f"[TESING] Skipping {game_name} for testing...")
        #    continue

        print(f"\nProcessing game: {game_name} (AppID: {game_appid}) ({count}/{total_games})")

        # Check if the 600x900 capsule cover image is a poor auto-conversion of the
        # old Big Picture wide banner using OCR
        # This image essentially is the wide banner shrunk down with a blurred background 
        #steam_librarycache_dir
        #steam_grid_dir
        header_image = os.path.join(steam_librarycache_dir, f"{game_appid}_header.jpg")
        capsule_image = os.path.join(steam_librarycache_dir, f"{game_appid}_library_600x900.jpg")
        print(f"Checking if {header_image} exists inside of {capsule_image}")
        missing_cover_art = ocr.check_image_contains_template(capsule_image, header_image)


        # TODO - download all cover art and process each style from SteamGridDB, not
        #        just the capsule cover art

        # https://www.steamgriddb.com/api/v2
        # {'id': 3120, 'name': 'A Hat in Time', 'release_date': 1507237200, 'types': ['steam', 'gog'], 'verified': True}
        try:
            steamgriddb_game = sgdb.get_game_by_steam_appid(int(game_appid)).to_json()
            grids = sgdb.get_grids_by_gameid(game_ids = [steamgriddb_game["id"]], dimensions = ["600x900"])
        except http.HTTPException:
            print(f"Game grid data not found for {game_name} ({game_appid})")
            continue

        if not grids:
            print(f"Game grid data not found for {game_name} ({game_appid})")
            continue

        # Process grid results
        for grid in grids:
            grid_json = grid.to_json()
            grid_image_url = grid_json["url"]
            grid_image_filetype= os.path.basename(grid_image_url).split('.')[1]

            # TODO - this part needs to be dynamic base don image type
            #        start with cover/capsule 600x900. For some reason that
            #        needs a "p" on the end (portrait?)
            grid_image_newfile = f"{game_appid}p.{grid_image_filetype}"

            # DEBUG
            # print(json.dumps(grid_json))

            # Same image with appropriate name
            # For automation, take the first result
            # Users can always use Decky Loader "steamgrid DB" plugin to adjust later

            # Cover art handling
            # Only download :
            #   * User wants to fix missing cover art
            #   * User does not* have args.only_missing set
            if (missing_cover_art and args.only_missing) or not args.only_missing:
                print(f"Downloading 600x900 capsule cover image: {grid_image_url} as {grid_image_newfile}")
                steam_helpers.download_grid_image(grid_image_newfile, grid_image_url, steam_grid_dir)
            else:
                print("Skipping capsule cover art download: Artwork not missing or --only-missing specified")


            # Need backoff mechanism for rate limiting?

            # Stop processing rest of grids
            break

    print("DONE!")
