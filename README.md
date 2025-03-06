# MusicPlayer

## Installation
You have to install these packages from pip :

* pip install tk
* pip install pygame
* pip install mutagen
* pip install ttkthemes
* pip install polib

## Generate application

### Windows
* pyinstaller --onefile --noconsole --icon=music_player.ico --add-data "controller;controller" --add-data "models;models" --add-data "views;views" main.py

### MacOS and Linux
* pyinstaller --onefile --noconsole --icon=music_player.ico --add-data "controller:controller" --add-data "models:models" --add-data "views:views" main.py

## Generate translations

* Go in scripts folder and execute generate_release. You can enable or disable some of the generation like translations or the executable.

## Code Location

### Controller :
Containing binds and the MainController of the project. Handle the input/output between the views and the models

### Locals :
Default folder to store the translations in different languages.

### Models :
All main classes such as the MusicPlayer, Songs, or the DirectoryListener

### Scripts : 
All scripts used for other purposes such as generate release or translations.

### Utils : 
Files providing help to the project like a configuration file, the translator,...

### Views : 
All graphical components should be stored in this folder

### Main.py : 
Entry point of the project