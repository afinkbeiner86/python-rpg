import pygame as pg
from pathlib import Path


class Weapon(pg.sprite.Sprite):
    """
    Represents a weapon that the player can use.

    Attributes:
        sprite_type (str): The type of sprite, used for collision handling.
        image (pygame.Surface): The weapon's image.
        rect (pygame.Rect): The rectangle defining the weapon's position and size.

    Args:
        player (Player): The player object to which this weapon belongs.
        groups (pygame.sprite.LayeredUpdates): The sprite groups to add this weapon to.

    """

    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split("_")[0]

        # Graphics
        weapons_path = Path("./assets/graphics/weapons/")
        weapon_image_path = weapons_path / player.weapon / f"{direction}.png"
        self.image = pg.image.load(str(weapon_image_path)).convert_alpha()

        # Offset
        offset_mapping = {
            "right": pg.math.Vector2(0, 16),
            "left": pg.math.Vector2(0, 16),
            "down": pg.math.Vector2(-10, 0),
            "up": pg.math.Vector2(-10, 0),
        }
        offset = offset_mapping[direction]

        # Placement
        if direction == "right":
            self.rect = self.image.get_rect(midleft=player.rect.midright + offset)
        elif direction == "left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + offset)
        elif direction == "down":
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + offset)
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + offset)
