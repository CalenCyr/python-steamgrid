#!/bin/python3

import os
from steamgriddy import SteamGridDB

# TODO
#   Add args
#   Add config (to hold API string with 400 user permissions)
#   Add Steam...
#       login
#       game parsing
#       data collection for current titles

# TESTING ONLY
if not os.envron["STEAM_API_KEY"]:
    exit("Please set your Steam API key to the env var 'STEAM_API_KEY'")
sgdb = SteamGridDB(os.envron["STEAM_API_KEY"])

# Get game data
game_data = sgdb.search_game('A Virus Named TOM')

# Print shit
print(game_data)
