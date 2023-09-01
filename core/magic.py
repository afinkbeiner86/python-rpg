import pygame as pg
from .settings import *
from random import randint


class MagicPlayer:
    """
    Represents a player with magical abilities for performing various actions.

    Attributes:
        animation_player (AnimationPlayer): The animation player associated with this magic player.

    Methods:
        heal(player, style, strength, cost, groups):
            Heal the player using magic, consuming energy and creating visual effects.
        flame(player, cost, groups):
            Generate a flame attack animation for the player, deducting energy if sufficient,
            and creating particles for visual effects.

    """

    def __init__(self, animation_player) -> None:
        """
        Initialize a MagicPlayer instance.

        Args:
            animation_player (AnimationPlayer): The AnimationPlayer object for managing animations.

        Returns:
            None

        """
        self.animation_player = animation_player

        self.heal_sound = pg.mixer.Sound(magic_data["heal"]["magic_sound"])
        self.flame_sound = pg.mixer.Sound(magic_data["flame"]["magic_sound"])
        self.heal_sound.set_volume(0.2)
        self.flame_sound.set_volume(0.1)

    def heal(self, player, strength, cost, groups):
        """
        Use magic to heal the player, consuming energy and creating visual effects.

        Args:
            player (Player): The player object to be healed.
            strength (int): The amount of health to be restored.
            cost (int): The energy cost of performing the healing magic.
            groups (pygame.sprite.LayeredUpdates): The sprite groups for particle effects.

        Returns:
            None

        Note:
            The function checks if the player's energy is sufficient and if the player's health is below maximum.
            If conditions are met, it restores the player's health by the specified strength, deducts energy,
            and triggers visual effects, including healing particles and an aura around the player's position.
            The player's health will not exceed the maximum health defined in their statistics.

        """
        if player.energy >= cost and player.health < player.stats["health"]:
            self.heal_sound.play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            self.animation_player.create_particles("heal", player.rect.center + pg.math.Vector2(0, -30), groups)
            self.animation_player.create_particles("aura", player.rect.center, groups)

    def flame(self, player, cost, groups):
        """
        Generate a flame attack animation for the player, deducting energy if sufficient,
        and creating particles for visual effects.

        Args:
            player (Player): The player object initiating the flame attack.
            cost (int): The energy cost of the flame attack.
            groups (pygame.sprite.LayeredUpdates): The sprite groups to add the flame particles to.

        Returns:
            None

        Notes:
            This function generates a flame attack animation based on the player's direction.
            It deducts energy as a cost and creates flame particles along the chosen direction.

        """
        if player.energy >= cost:
            self.flame_sound.play()
            player.energy -= cost

            # Determine the direction the player is facing
            direction = self.get_player_direction(player)

            # Create flame particles along the chosen direction
            for i in range(1, 6):
                if direction.x:  # Horizontal direction
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles("flame", (x, y), groups)
                else:  # Vertical direction
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles("flame", (x, y), groups)

    def get_player_direction(self, player):
        """
        Determine the direction the player is facing.

        Args:
            player (Player): The player object.

        Returns:
            pg.math.Vector2: The direction vector (x, y) indicating the player's facing direction.

        """
        status_parts = player.status.split("_")
        if status_parts[0] == "right":
            return pg.math.Vector2(1, 0)
        elif status_parts[0] == "left":
            return pg.math.Vector2(-1, 0)
        elif status_parts[0] == "up":
            return pg.math.Vector2(0, -1)
        else:
            return pg.math.Vector2(0, 1)
