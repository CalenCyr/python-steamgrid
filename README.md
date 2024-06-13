# python-steamgridddy

Forked from: https://github.com/ZebcoWeb/python-steamgriddb. Core bits inspired by https://github.com/boppreh/steamgrid.

This program's main aim is to fixup Steam artwork for common use cases. The most common issue is the horrid "cover art" for 600x900 capsule covers on Steam Deck (SteamOS v3) that are nothing more than the old wide banner shrunk with a blurred background. In due time, I want to add some more functionality, but that is the main aim. This is meant to ideally be a quick fixer utility. For a proper artwork manager, please see the desktop application https://github.com/Tormak9970/Steam-Art-Manager.

Thank you to ZebcoWeb for the API code for SteamGridDB.

[![PyPI](https://img.shields.io/pypi/v/python-steamgriddy?style=for-the-badge)](https://pypi.python.org/pypi/python-steamgriddy)
![APM](https://img.shields.io/apm/l/github?style=for-the-badge)

### Installation
```shell
pip install -U python-steamgriddy
```
or
```shell
pip install -U git+https://github.com/ZebcoWeb/python-steamgriddy.git
```

## Setup and configuration 

TODO....

## API

#### Get your API key:
[You can generate an API key on your user preferences page.](https://www.steamgriddb.com/profile/preferences)


Initialize the SteamGridDB using your API key to connect with API
```python
from steamgrid import SteamGridDB

sgdb = SteamGridDB('AuthKey')
```

#### Search for a game:
```python
# Search for Witcher game
result = sgdb.search_game('Witcher')
```

#### Get a game object without searching:
```python
# Get a game using a Game ID
game = sgdb.get_game_by_gameid(1234)

# Get a game using Steam App ID
game = sgdb.get_game_by_steam_appid(567890)

# Returning the game as JSONObject
game.to_json()
```

#### Do something with a game object:
```python
# Return the game name
game_name = game.name

# Return the game release date as datetime
game_release_date = game.release_date
```

#### Get Assets:
```python
from steamgrid import StyleType, PlatformType, MimeType, ImageType

# Get grids list without filter
grids = sgdb.get_grids_by_gameid([1234])

# Get grids with a specific demension (e.g. 600x900 cover capsules)
grids = sgdb.get_grids_by_gameid(game_ids=[1234], dimensions=["600x900"])

# Get grids list by filter (Multiple filters are allowed)
grids = sgdb.get_grids_by_gameid(game_ids=[1234], styles=[StyleType.Alternate], mimes=[MimeType.PNG], types=[ImageType.Static], is_nsfw=True)

# Get list grids using platform
grids = sgdb.get_grids_by_platform(game_ids=[1234], platform=PlatformType.origin)
```

#### Do something with a grid object:
```python
# Return object of grid's author
grid_author = grid.author

# Return grid's score
grid_score = grid.score
```

#### Some grid object methods:
```python
# Return true if grid be nsfw
grid_is_nsfw = grid.is_nsfw()

# Returning the grid as JSONObject
grid.to_json()
```

#### Delete a grid
```python
# Delete a grid with its object
grid.delete()

# Delete a grid with its ID
sgdb.delete_grid([230227])
```

