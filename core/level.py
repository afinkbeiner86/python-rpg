from typing import Iterable, Tuple, Union
import pathlib
import pygame as pg
from random import choice, randint
from pygame.sprite import AbstractGroup
from .settings import *
from .helper import *
from .tile import Tile
from .player import Player
from .enemy import Enemy
from .weapon import Weapon
from .particles import AnimationPlayer
from .ui import UI
from .magic import MagicPlayer
from .upgrade import Upgrade


class Level:
    """
    Represents a game level.

    This class manages the game environment, including map creation,
    player interactions, sprite groups, and user interface.

    Attributes:
        display_surface (pygame.Surface): The display surface for rendering.
        game_paused (bool): Flag to indicate if the game is paused.
        visible_sprites (YSortCameraGroup): A sprite group for visible objects.
        obstacle_sprites (YSortCameraGroup): A sprite group for obstacles.
        current_attack (Weapon): The currently active player attack.
        attack_sprites (pygame.sprite.Group): A group for attack-related sprites.
        attackable_sprites (pygame.sprite.Group): A group for sprites that can be attacked.
        ui (UI): The user interface for the game.
        upgrade (Upgrade): The upgrade menu for the player.
        animation_player (AnimationPlayer): Manages particle animations.
        magic_player (MagicPlayer): Manages player magic abilities.
        player (Player): The player character in the level.

    Methods:
        create_map(): Create the game map, including tiles and entities.
        create_attack(): Create a player attack.
        destroy_attack(): Destroy the current player attack.
        create_magic(style: str, strength: int, cost: int): Create player magic.
        player_attack_logic(): Manage player attacks and damage calculation.
        damage_player(amount: int, attack_type: str): Damage the player character.
        trigger_death_particles(pos: Tuple[int, int], particle_type: str): Trigger death particle animations.
        trigger_magic_particles(pos: Tuple[int, int], particle_type: str): Trigger magic particle animations.
        add_xp(amount: int): Add experience points to the player.
        toggle_menu(): Toggle the game menu.
        run(): Run the game loop.

    """

    def __init__(self) -> None:
        """
        Initialize a new game level.

        This constructor sets up the game environment, including sprite groups,
        player, user interface, and particle managers.
        """

        # Get display surface
        self.display_surface = pg.display.get_surface()
        self.game_paused = False

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = YSortCameraGroup()

        # Attack sprites
        self.current_attack = None
        self.attack_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()

        # Sprite setup
        self.create_map()

        # User interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # Particle animation
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        """
        Create the game map based on layout and graphics files.

        This method reads layout and graphics files to create the game map.
        It places tiles and entities based on the layout files.
        """

        layout_files = {
            "boundary": "./assets/map/map_FloorBlocks.csv",
            "grass": "./assets/map/map_Grass.csv",
            "object": "./assets/map/map_LargeObjects.csv",
            "entities": "./assets/map/map_Entities.csv",
        }
        graphics_folders = {
            "grass": "./assets/graphics/grass",
            "objects": "./assets/graphics/objects",
        }

        for style, layout_file in layout_files.items():
            layout = import_csv_layout(Path(layout_file))
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != "-1":
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == "boundary":
                            Tile((x, y), self.obstacle_sprites, "invisible")
                        elif style == "grass":
                            random_grass = choice(import_folder(Path(graphics_folders["grass"])))
                            Tile(
                                (x, y),
                                [self.obstacle_sprites, self.visible_sprites, self.attackable_sprites],
                                "grass",
                                random_grass,
                            )
                        elif style == "object":
                            surface = import_folder(Path(graphics_folders["objects"]))[int(column)]
                            Tile((x, y), [self.obstacle_sprites, self.visible_sprites], "object", surface)
                        elif style == "entities":
                            if column == "394":
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                )
                            else:
                                monster_name = {
                                    "390": "bamboo",
                                    "391": "spirit",
                                    "392": "raccoon",
                                }.get(column, "squid")

                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_xp,
                                )

    def create_attack(self) -> None:
        """
        Create a player attack.

        This method creates a new player attack instance and assigns it to the
        'current_attack' attribute of the level.

        Returns:
            None
        """

        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self) -> None:
        """
        Destroy the current player attack.

        This method checks if there is a current player attack and removes it
        from the game by calling its 'kill' method. It then sets 'current_attack'
        to None.

        Returns:
            None
        """

        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self, style: str, strength: int, cost: int) -> None:
        """
        Create player magic.

        This method creates and activates player magic abilities based on the
        specified 'style'. If the style is 'heal', it triggers the 'heal' magic,
        and if it's 'flame', it triggers the 'flame' magic. The magic actions
        affect the player and other game elements as defined by the game logic.

        Args:
            style (str): The style of magic ('heal' or 'flame').
            strength (int): The strength or power of the magic.
            cost (int): The cost or resource required to use the magic.

        Returns:
            None
        """

        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self) -> None:
        """
        Manage player attacks and damage calculation.

        This method handles player attacks by checking for collisions between
        player attack sprites and attackable sprites. Depending on the collision
        results, it triggers damage or other effects on the target sprites.

        Returns:
            None
        """

        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pg.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount: int, attack_type: str) -> None:
        """
        Damage the player character.

        This method inflicts damage on the player character based on the 'amount'
        and 'attack_type'. It also handles the player's health and vulnerability
        states and triggers particle animations upon damage.

        Args:
            amount (int): The amount of damage to inflict on the player.
            attack_type (str): The type of attack causing the damage.

        Returns:
            None
        """

        if self.player.vulnerable:
            if self.player.health > 0:
                self.player.health -= amount
            else:
                self.player.health = 0
            self.player.vulnerable = False
            self.player.hurt_time = pg.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos: Tuple[int, int], particle_type: str) -> None:
        """
        Trigger death particle animations.

        This method triggers particle animations for character death effects
        at the specified 'pos' with the given 'particle_type'.

        Args:
            pos (Tuple[int, int]): The position at which to trigger the particle animation.
            particle_type (str): The type of death particle animation.

        Returns:
            None
        """

        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def trigger_magic_particles(self, pos: Tuple[int, int], particle_type: str) -> None:
        """
        Trigger magic particle animations.

        This method triggers particle animations for magic effects at the specified
        'pos' with the given 'particle_type'.

        Args:
            pos (Tuple[int, int]): The position at which to trigger the particle animation.
            particle_type (str): The type of magic particle animation.

        Returns:
            None
        """

        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_xp(self, amount: int) -> None:
        """
        Add experience points to the player.

        This method adds the specified 'amount' of experience points to the player's
        experience attribute.

        Args:
            amount (int): The amount of experience points to add.

        Returns:
            None
        """

        self.player.experience += amount

    def toggle_menu(self) -> None:
        """
        Toggle the game menu.

        This method toggles the game menu's visibility by changing the 'game_paused'
        attribute between True and False.

        Returns:
            None
        """

        self.game_paused = not self.game_paused

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            # Display upgrade menu
            self.upgrade.display()
        else:
            # Draw and update game
            self.visible_sprites.update()
            self.visible_sprites.update_enemy(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pg.sprite.Group):
    """
    A specialized sprite group for camera sorting.

    This sprite group is designed for camera sorting in the game.
    It includes methods for custom drawing and updating enemy sprites.

    Attributes:
        display_surface (pygame.Surface): The display surface for rendering.
        half_width (int): Half of the display width.
        half_height (int): Half of the display height.
        offset (pg.math.Vector2): The camera offset.
        floor_surface_image (pathlib.Path): The path to the floor surface image.
        floor_surface (pygame.Surface): The floor surface for the background.
        floor_rect (pygame.Rect): The rect of the floor surface.

    Methods:
        custom_draw(player: Player): Custom drawing of sprites with camera offset.
        update_enemy(player: Player): Update enemy sprites in the group.

    """

    def __init__(self, *sprites: Union[AbstractGroup, Iterable]) -> None:
        """
        Initialize a YSortCameraGroup.

        This constructor sets up the camera group and initializes related attributes.

        Args:
            *sprites (Union[AbstractGroup, Iterable]): Sprite groups and iterable sprites to include in the group.
        """

        super().__init__(*sprites)

        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2(100, 200)

        # Create the floor surface
        self.floor_surface_image = pathlib.Path("./assets/graphics/tilemap/ground.png")
        self.floor_surface = pg.image.load(self.floor_surface_image).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player: Player) -> None:
        """
        Custom drawing of sprites with camera offset.

        This method draws sprites with consideration of the camera offset to create the illusion of a moving camera.

        Args:
            player (Player): The player character used to determine the camera offset.
        """

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def update_enemy(self, player: Player) -> None:
        """
        Update enemy sprites in the group.

        This method updates enemy sprites based on player interactions and positions.

        Args:
            player (Player): The player character used for enemy updates.
        """

        enemy_sprites = [
            sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for sprite in enemy_sprites:
            sprite.update_enemy(player)
