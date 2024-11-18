# MusicPlayer

## Installation
You have to install these packages from pip :

* pip install tk
* pip install pygame
* pip install mutagen
* pip install ttkthemes

## Generate application

### Windows
* pyinstaller --onefile --noconsole --icon=music_player.ico --add-data "controller;controller" --add-data "models;models" --add-data "views;views" main.py

### MacOS and Linux
* pyinstaller --onefile --noconsole --icon=music_player.ico --add-data "controller:controller" --add-data "models:models" --add-data "views:views" main.py
