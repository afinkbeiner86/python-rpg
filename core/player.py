import pygame as pg
from pathlib import Path
from .settings import *
from .entity import Entity
from .helper import import_folder


class Player(Entity):
    """
    Represents the player character in the game.

    Attributes:
        image (pygame.Surface): The player's image.
        rect (pygame.Rect): The player's position and size.
        hitbox (pygame.Rect): The player's hitbox for collision detection.
        animations (dict): Dictionary containing player animations.
        status (str): Current player status (e.g., "up", "down", "left").
        speed (int): Player's movement speed.
        attacking (bool): Indicates if the player is currently attacking.
        attack_cooldown (int): Cooldown duration for attacks.
        attack_time (int): Time of the last attack.
        obstacle_sprites (pygame.sprite.Group): Group of obstacle sprites.
        create_attack (function): Function to create player attacks.
        destroy_attack (function): Function to destroy player attacks.
        weapon_index (int): Index of the player's current weapon.
        weapon_list (list): List of available weapons.
        weapon (str): Current weapon equipped by the player.
        can_switch_weapon (bool): Indicates if the player can switch weapons.
        weapon_switch_time (int): Time of the last weapon switch.
        switch_cooldown_duration (int): Cooldown duration for switching weapons.
        create_magic (function): Function to create magic attacks.
        magic_index (int): Index of the player's current magic spell.
        magic_list (list): List of available magic spells.
        magic (str): Current magic spell used by the player.
        can_switch_magic (bool): Indicates if the player can switch magic spells.
        magic_switch_time (int): Time of the last magic spell switch.
        stats (dict): Player's statistics (health, energy, attack, magic, speed).
        max_stats (dict): Maximum values for player statistics.
        upgrade_cost (dict): Cost of upgrading player statistics.
        health (int): Current health points of the player.
        energy (int): Current energy points of the player.
        experience (int): Player's experience points.
        vulnerable (bool): Indicates if the player can take damage.
        hurt_time (int): Time of the last damage taken.
        invulnerability_duration (int): Duration of invulnerability after taking damage.
        player_attack_sound (pygame.mixer.Sound): Sound played when the player attacks.

    Methods:
        import_player_assets(): Import player animations from files.
        input(): Handle player input for movement and attacks.
        cooldowns(): Manage attack and switch cooldowns.
        get_status(): Update the player's status based on input and actions.
        animate(): Animate the player character.
        get_full_weapon_damage(): Calculate the total damage including the weapon.
        get_full_magic_damage(): Calculate the total magic damage.
        get_value_by_index(index): Get the player's statistic value by index.
        get_cost_by_index(index): Get the cost of upgrading a statistic by index.
        energy_recovery(): Handle energy recovery over time.
        update(): Update the player's state and actions in the game.
    """

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic) -> None:
        """
        Initialize a new Player instance.

        Args:
            pos (tuple): Initial position of the player.
            groups (list): Groups to which the player belongs.
            obstacle_sprites (pygame.sprite.Group): Group of obstacle sprites.
            create_attack (function): Function to create player attacks.
            destroy_attack (function): Function to destroy player attacks.
            create_magic (function): Function to create magic attacks.
        """
        super().__init__(groups)
        self.image = pg.image.load(PLAYER_SPAWN_SPRITE).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])

        # graphics setup
        self.import_player_assets()
        self.status = "down"

        # movement
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon_list = list(weapon_data.keys())
        self.weapon = self.weapon_list[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_cooldown_duration = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic_list = list(magic_data.keys())
        self.magic = self.magic_list[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 6}
        self.max_stats = {"health": 300, "energy": 140, "attack": 20, "magic": 10, "speed": 10}
        self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.experience = 0

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # sounds
        self.player_attack_sound = pg.mixer.Sound(sound_data["player_hit"])
        self.player_attack_sound.set_volume(0.1)

    def import_player_assets(self):
        """
        Import player animations from files.
        """
        character_path = Path("./assets/graphics/player/")
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_attack": [],
            "left_attack": [],
            "up_attack": [],
            "down_attack": [],
        }

        for animation in self.animations.keys():
            full_path = Path.joinpath(character_path, animation)
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """
        Handle player input for movement and attacks.
        """
        if not self.attacking:
            keys = pg.key.get_pressed()

            # movement input
            if keys[pg.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pg.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pg.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # combat input
            if keys[pg.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()
                self.create_attack()
                self.player_attack_sound.play()

            if keys[pg.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pg.time.get_ticks()

                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
                cost = list(magic_data.values())[self.magic_index]["cost"]

                self.create_magic(style, strength, cost)

            if keys[pg.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pg.time.get_ticks()

                if self.weapon_index >= len(self.weapon_list) - 1:
                    self.weapon_index = 0
                else:
                    self.weapon_index += 1
                self.weapon = self.weapon_list[self.weapon_index]

            if keys[pg.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pg.time.get_ticks()

                if self.magic_index >= len(self.magic_list) - 1:
                    self.magic_index = 0
                else:
                    self.magic_index += 1
                self.magic = self.magic_list[self.magic_index]

    def cooldowns(self):
        """
        Manage attack and switch cooldowns.
        """
        current_time = pg.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]["cooldown"]:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_cooldown_duration:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_cooldown_duration:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def get_status(self):
        """
        Update the player's status based on input and actions.
        """
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def animate(self):
        """
        Animate the player character.
        """
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set asset for animation
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker player if damage is taken
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        """
        Calculate the total damage including the weapon.
        """
        base_damage = self.stats["attack"]
        weapon_damage = weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        """
        Calculate the total magic damage.
        """
        base_damage = self.stats["magic"]
        spell_damage = magic_data[self.magic]["strength"]
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        """
        Get the player's statistic value by index.

        Args:
            index (int): Index of the statistic to retrieve.

        Returns:
            int: Value of the specified statistic.
        """
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        """
        Get the cost of upgrading a statistic by index.

        Args:
            index (int): Index of the statistic cost to retrieve.

        Returns:
            int: Cost of upgrading the specified statistic.
        """
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        """
        Handle energy recovery over time.
        """
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def update(self):
        """
        Update the player's state and actions in the game.
        """
        self.input()
        self.cooldowns()
        self.get_status()
        self.move(self.stats["speed"])
        self.animate()
        self.energy_recovery()
