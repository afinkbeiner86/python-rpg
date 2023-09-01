import pygame as pg
from .settings import TILESIZE, HITBOX_OFFSET


class Tile(pg.sprite.Sprite):
    """
    Represents a tile in the game world.

    Attributes:
        sprite_type (str): The type of the tile, e.g., "object", "grass", etc.
        image (pygame.Surface): The image representing the tile.
        rect (pygame.Rect): The rectangular region occupied by the tile.
        hitbox (pygame.Rect): The hitbox used for collision detection.

    Methods:
        __init__(self, pos, groups, sprite_type, surface=pg.Surface((TILESIZE, TILESIZE))):
            Initialize a Tile instance with the specified attributes.
    """

    def __init__(self, pos, groups, sprite_type, surface=pg.Surface((TILESIZE, TILESIZE))) -> None:
        """
        Initialize a Tile instance.

        Args:
            pos (tuple): The position of the tile (x, y) on the game grid.
            groups (list): A list of sprite groups to which the tile belongs.
            sprite_type (str): The type of the tile, e.g., "object", "grass", etc.
            surface (pygame.Surface, optional): The image surface for the tile. Defaults to a blank surface.

        Returns:
            None
        """
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)
