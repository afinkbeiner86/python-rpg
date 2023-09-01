import pygame as pg
from pathlib import Path
from .helper import import_folder
from random import choice

# Define the base path to your assets directory
ASSETS_PATH = Path("./assets")


class AnimationPlayer:
    """
    Handles the animation frames for various in-game animations.

    Attributes:
        frames (dict): A dictionary containing animation frames for different animation types.

    Methods:
        load_frames(folder_name):
            Load animation frames from the specified folder.

        load_leaf_frames():
            Load and structure animation frames for leaf animations.

        reflect_images(frames):
            Create a mirrored version of animation frames.

        create_grass_particles(pos, groups):
            Create grass particles at the specified position.

        create_particles(animation_type, pos, groups):
            Create particles of the specified animation type at the specified position.

    """

    def __init__(self) -> None:
        """
        Initialize an AnimationPlayer instance with animation frames.

        Returns:
            None

        """
        self.frames = {
            "flame": self.load_frames("particles/flame/frames"),
            "aura": self.load_frames("particles/aura"),
            "heal": self.load_frames("particles/heal/frames"),
            "claw": self.load_frames("particles/claw"),
            "slash": self.load_frames("particles/slash"),
            "sparkle": self.load_frames("particles/sparkle"),
            "leaf_attack": self.load_frames("particles/leaf_attack"),
            "thunder": self.load_frames("particles/thunder"),
            "squid": self.load_frames("particles/smoke_orange"),
            "raccoon": self.load_frames("particles/raccoon"),
            "spirit": self.load_frames("particles/nova"),
            "bamboo": self.load_frames("particles/bamboo"),
            "leaf": self.load_leaf_frames(),
        }

    def load_frames(self, folder_name):
        """
        Load animation frames from a specified folder.

        Args:
            folder_name (str): The name of the folder containing animation frames.

        Returns:
            list: A list of loaded animation frames.

        """
        folder_path = ASSETS_PATH / f"graphics/{folder_name}"
        return import_folder(folder_path)

    def load_leaf_frames(self):
        """
        Load and structure animation frames for leaf animations.

        Returns:
            list: A list of structured leaf animation frames.

        """
        leaf_frames = []
        for i in range(1, 7):
            frames = self.load_frames(f"particles/leaf{i}")
            leaf_frames.extend([frames, self.reflect_images(frames)])
        return leaf_frames

    def reflect_images(self, frames):
        """
        Create a mirrored version of animation frames.

        Args:
            frames (list): The list of animation frames to be mirrored.

        Returns:
            list: A list of mirrored animation frames.

        """
        return [pg.transform.flip(frame, True, False) for frame in frames]

    def create_grass_particles(self, pos, groups):
        """
        Create grass particles at the specified position.

        Args:
            pos (tuple): The position (x, y) to create the particles.
            groups (pygame.sprite.LayeredUpdates): The sprite groups to add particles to.

        Returns:
            None

        """
        animation_frames = choice(self.frames["leaf"])
        ParticleEffects(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        """
        Create particles of the specified animation type at the specified position.

        Args:
            animation_type (str): The type of animation to create.
            pos (tuple): The position (x, y) to create the particles.
            groups (pygame.sprite.LayeredUpdates): The sprite groups to add particles to.

        Returns:
            None

        """
        animation_frames = self.frames[animation_type]
        if animation_frames:
            ParticleEffects(pos, animation_frames, groups)


class ParticleEffects(pg.sprite.Sprite):
    """
    Represents an individual particle effect.

    Attributes:
        sprite_type (str): The type of sprite, e.g., "magic".
        frame_index (float): The index of the current animation frame.
        animation_speed (float): The speed at which the animation plays.
        frames (list): A list of animation frames.
        image (pygame.Surface): The current image of the particle.
        rect (pygame.Rect): The rectangular bounds of the particle.

    Methods:
        animate():
            Advance the animation frame of the particle.

        update():
            Update the particle's animation frame.

    """

    def __init__(self, pos, animation_frames, groups) -> None:
        """
        Initialize a ParticleEffects instance.

        Args:
            pos (tuple): The initial position (x, y) of the particle.
            animation_frames (list): A list of animation frames.
            groups (pygame.sprite.LayeredUpdates): The sprite groups to add the particle to.

        Returns:
            None

        """
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Advance the animation frame of the particle.

        Returns:
            None

        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
        Update the particle's animation frame.

        Returns:
            None

        """
        self.animate()
