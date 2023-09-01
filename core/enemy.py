import pygame as pg
from .settings import *
from .entity import Entity
from .helper import *
from pathlib import Path


class Enemy(Entity):
    """
    Class representing an enemy entity in the game.

    Attributes:
        monster_name (str): The name of the monster.
        pos (tuple): The initial position of the enemy.
        groups (pygame.sprite.Group): The sprite groups to which this enemy belongs.
        obstacle_sprites (pygame.sprite.Group): The group of obstacle sprites.
        damage_player (function): A function to deal damage to the player.
        trigger_death_particles (function): A function to trigger death particles.
        add_xp (function): A function to add experience points to the player.
    """

    def __init__(
        self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_xp
    ) -> None:
        """
        Initializes an enemy instance.

        Args:
            monster_name (str): The name of the monster.
            pos (tuple): The initial position of the enemy.
            groups (pygame.sprite.Group): The sprite groups to which this enemy belongs.
            obstacle_sprites (pygame.sprite.Group): The group of obstacle sprites.
            damage_player (function): A function to deal damage to the player.
            trigger_death_particles (function): A function to trigger death particles.
            add_xp (function): A function to add experience points to the player.
        """
        super().__init__(groups)

        # General setup
        self.sprite_type = "enemy"

        # Graphics setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.init_stats(monster_info)

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 600
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_xp = add_xp

        # Invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # Sounds
        self.enemy_death = pg.mixer.Sound(sound_data["death"])
        self.enemy_hit = pg.mixer.Sound(sound_data["enemy_hit"])
        self.attack_sound = pg.mixer.Sound(monster_info["attack_sound"])
        for sound in [self.enemy_death, self.enemy_hit, self.attack_sound]:
            sound.set_volume(0.1)

    def init_stats(self, monster_info):
        """
        Initializes the statistics of the enemy based on monster_info.

        Args:
            monster_info (dict): Information about the monster's stats.
        """
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

    def import_graphics(self, name):
        """
        Imports graphics/animations for the enemy.

        Args:
            name (str): The name of the enemy.
        """
        self.animations = {"idle": [], "move": [], "attack": []}
        monsters_path = Path("./assets/graphics/monsters/")
        monster_path = Path.joinpath(monsters_path, name)

        for animation in self.animations.keys():
            full_path = Path.joinpath(monster_path, animation)
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        """
        Calculates the distance and direction between the enemy and the player.

        Args:
            player (Player): The player object.

        Returns:
            tuple: A tuple containing the distance and direction vectors.
        """
        enemy_vector = pg.math.Vector2(self.rect.center)
        player_vector = pg.math.Vector2(player.rect.center)

        # Subtract player and enemy vector, then use magnitude()
        # to get the distance between both vectors
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pg.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        """
        Determines the enemy's current status based on the player's distance.

        Args:
            player (Player): The player object.
        """
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.stauts = "idle"

    def actions(self, player):
        """
        Performs actions based on the enemy's current status.

        Args:
            player (Player): The player object.
        """
        if self.status == "attack":
            self.attack_time = pg.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pg.math.Vector2()

    def get_damage(self, player, attack_type):
        """
        Inflicts damage on the enemy and sets invincibility timer if vulnerable.

        Args:
            player (Player): The player object.
            attack_type (str): The type of attack (e.g., "weapon" or "magic").
        """
        if self.vulnerable:
            self.enemy_hit.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()

            self.hit_time = pg.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        """
        Checks if the enemy's health has reached zero and triggers death actions.
        """
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_xp(self.exp)
            self.enemy_death.play()

    def hit_reaction(self):
        """
        Modifies the enemy's direction if it's not vulnerable.
        """
        if not self.vulnerable:
            self.direction *= -self.resistance

    def animate(self):
        """
        Animates the enemy's sprite.
        """
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Flicker enemy if damaged
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        """
        Manages cooldowns for attacking and invincibility.
        """
        current_time = pg.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def update(self):
        """
        Updates the enemy's behavior and attributes.
        """
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def update_enemy(self, player):
        """
        Updates the enemy's status and actions based on the player's position.

        Args:
            player (Player): The player object.
        """
        self.get_status(player)
        self.actions(player)
        self.check_death()
