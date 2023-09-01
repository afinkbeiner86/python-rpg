import pygame as pg
from math import sin


class Entity(pg.sprite.Sprite):
    """
    Represents an entity in the game, such as a player or enemy.

    Attributes:
        frame_index (int): Index for the current frame of animation.
        animation_speed (float): Speed of animation playback.
        direction (pg.math.Vector2): Current direction of the entity's movement.

    Args:
        groups (pygame.sprite.LayeredUpdates): The sprite groups to add this entity to.

    """

    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pg.math.Vector2()

    def move(self, speed):
        """
        Move the entity in the specified direction at the given speed.

        Args:
            speed (float): The speed at which the entity should move.

        Returns:
            None

        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        Handle collision detection and response with obstacles.

        Args:
            direction (str): The direction of collision detection, either "horizontal" or "vertical".

        Returns:
            None

        """
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        """
        Create alpha values for flickering hit reaction using a sine wave.

        Returns:
            int: The alpha value (0 or 255) for flickering effect.

        """
        value = sin(pg.time.get_ticks())
        return 255 if value >= 0 else 0
