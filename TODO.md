# TODO list

## cli.py
* Add args
* Add config (to hold API string with 400 user permissions)

## Libs

### steamgriddy.py

* Method to fetch grid image URL object via requests

### steam_helper.py
* Method to use steamgriddy lib to initiate image download, and save it in the appropriate folder with the appropriate name
  * `<GAME_ID>.png` (main image for cover used per `/grid/` folder examples)
  * `<GAME_ID>_icon.png`
  * `<GAME_ID>_hero.png`
  * `<GAME_ID>_logo.jpg`
