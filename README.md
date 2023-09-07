# TerraMythica

## Introduction

This project has been built while following along one of [ClearCode's](https://www.youtube.com/@ClearCode/) magnificant coding tutorials.   
I had little experience with pygame so this was literally quite the adventure.  
My intention was to figure out most of the stuff on my own, do some refactoring and add docstrings to the code.  
  
But mostly, completing this project was a lot of fun and it's an awesome feeling to see the game coming together feature by feature!

## State

Mind that the game is working with its features but still incomplete!

- There is no player death / respawn mechanic
- There is no savegame or state mechanic
- There is no monster respawn mechanic

## Controls
  
| Action | Key |
|---|---|
| Movement | W A S D |
| Attack | Space |
| Cast Spell | Left CTRL |
| Switch Weapon | Q |
| Switch Magic | E |
| Upgrade Menu | M |
| Navigate Menu | Cursor Keys |
| Upgrade | Space |

## Download and play
If you are on Windows hop to the [Release section](https://github.com/jimsemara/python-rpg/releases) and download the latest release.

For other platforms you have to build from source.  

## Build
This project has been built and tested with Python 3.11.4.
  
**From source:**
```sh
# Clone the project locally
# Install dependencies:
    pip install -r requirements.txt
# Run game:
    python ./terramythica.py
```
  
**Build Windows binary:**
```sh
# Clone the project locally
# Install dependencies:
    pip install --upgrade cx_Freeze
# Build binary:
    python setup.py build
# Or use make:
    make build-exe
```

**Cleanup build files:**
```sh
make cleanup
```

## License
This project is published under the Creative Commons Zero (CC0) license by ClearCode (Christian Koch).  
[ClearCode's Project Repo](https://github.com/clear-code-projects/Zelda)
  
The assets used in this project are released under the Creative Commons Zero (CC0) license by
  
[Pixel-Boy](https://twitter.com/2Pblog1) and [AAA](https://www.instagram.com/challenger.aaa/?hl=fr)
  
Link to their [Patreon](https://www.patreon.com/pixelarchipel)

Project is built with cx_Freeze: [License for cx_Freeze](https://cx-freeze.readthedocs.io/en/stable/license.html#license-for-cx-freeze)

## Sources
**ClearCode:**

[YouTube Channel](https://www.youtube.com/@ClearCode/)

[Project Repo](https://github.com/clear-code-projects/Zelda)
  
**Assets:**

[NinjaAdventureAssetPack](https://pixel-boy.itch.io/ninja-adventure-asset-pack)
