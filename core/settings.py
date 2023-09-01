from pathlib import Path


# Game configuration

# Screen dimensions
WIDTH = 1280
HEIGHT = 720

# Frames per second
FPS = 60

# Tile size (used for grid-based games)
TILESIZE = 64

# Hitbox offsets for various game objects

HITBOX_OFFSET = {"player": -26, "object": -40, "grass": -10, "invisible": 0}

# Path to the player object spawn sprite
PLAYER_SPAWN_SPRITE = Path("./assets/graphics/player/down/down_0.png")

# Path to the window icon
WINDOW_ICON = Path("./assets/graphics/icon/02.png")


# Sound Configuration

# Main game music
MAIN_MUSIC = Path("./assets/audio/main.ogg")

# Sound effects data
sound_data = {
    "death": Path("./assets/audio/death.wav"),
    "enemy_hit": Path("./assets/audio/enemy_hit.wav"),
    "player_hit": Path("./assets/audio/player_hit.wav"),
}


# User Interface Configuration

# Height of various UI elements
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80

# Path to the UI font
UI_FONT = Path("./assets/graphics/font/joystix.ttf")

# Font size for UI elements
UI_FONT_SIZE = 18


# General Colors

# Water color for the game background
WATER_COLOR = "#71ddee"

# Background color for UI elements
UI_BG_COLOR = "#222222"

# Border color for UI elements
UI_BORDER_COLOR = "#111111"

# Text color for UI elements
TEXT_COLOR = "#EEEEEE"


# UI Colors

# Health bar color
HEALTH_COLOR = "red"

# Energy bar color
ENERGY_COLOR = "blue"

# Border color for active UI elements
UI_BORDER_COLOR_ACTIVE = "gold"


# Upgrade Menu Configuration

# Text color for selected items in the upgrade menu
TEXT_COLOR_SELECTED = "#111111"

# Bar color for upgrade menu items
BAR_COLOR = "#EEEEEE"

# Bar color for selected upgrade menu items
BAR_COLOR_SELECTED = "#111111"

# Background color for selected upgrade menu items
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"


# Weapon Data Configuration

# Data for different weapon types
weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": Path("./assets/graphics/weapons/sword/full.png")},
    "lance": {"cooldown": 400, "damage": 30, "graphic": Path("./assets/graphics/weapons/lance/full.png")},
    "axe": {"cooldown": 300, "damage": 20, "graphic": Path("./assets/graphics/weapons/axe/full.png")},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": Path("./assets/graphics/weapons/rapier/full.png")},
    "sai": {"cooldown": 80, "damage": 10, "graphic": Path("./assets/graphics/weapons/sai/full.png")},
}


# Magic Data Configuration

# Data for different magic spells
magic_data = {
    "flame": {
        "strength": 5,
        "cost": 20,
        "graphic": Path("./assets/graphics/particles/flame/fire.png"),
        "magic_sound": Path("./assets/audio/flame.wav"),
    },
    "heal": {
        "strength": 20,
        "cost": 10,
        "graphic": Path("./assets/graphics/particles/heal/heal.png"),
        "magic_sound": Path("./assets/audio/heal.wav"),
    },
}


# Enemy Data Configuration

# Data for different enemy types
monster_data = {
    "squid": {
        "health": 100,
        "exp": 100,
        "damage": 10,
        "attack_type": "slash",
        "attack_sound": Path("./assets/audio/attack/slash.wav"),
        "speed": 3,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "raccoon": {
        "health": 300,
        "exp": 250,
        "damage": 40,
        "attack_type": "claw",
        "attack_sound": Path("./assets/audio/attack/claw.wav"),
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "spirit": {
        "health": 100,
        "exp": 110,
        "damage": 8,
        "attack_type": "thunder",
        "attack_sound": Path("./assets/audio/attack/fireball.wav"),
        "speed": 4,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 350,
    },
    "bamboo": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "leaf_attack",
        "attack_sound": Path("./assets/audio/attack/slash.wav"),
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
