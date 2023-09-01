import pygame as pg
from .settings import *


class UI:
    def __init__(self) -> None:
        """
        Initialize the User Interface (UI) for displaying player information and game elements.

        This class manages the graphical representation of player statistics, such as health and energy bars,
        experience points, and selection boxes for weapons and magic.

        Attributes:
            display_surface (pygame.Surface): The game display surface.
            font (pygame.font.Font): The font used for rendering text.
            health_bar_rect (pygame.Rect): The rectangle for the health bar.
            energy_bar_rect (pygame.Rect): The rectangle for the energy bar.
            weapon_graphics (list): A list of weapon graphics (pygame.Surface) for selection boxes.
            magic_graphics (list): A list of magic style graphics (pygame.Surface) for selection boxes.

        Returns:
            None

        """
        # General
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pg.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pg.Rect(10, 34, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        # Convert weapon data dictionary
        self.weapon_graphics = [pg.image.load(weapon["graphic"]).convert_alpha() for weapon in weapon_data.values()]

        # Convert magic data dictionary
        self.magic_graphics = [pg.image.load(style["graphic"]).convert_alpha() for style in magic_data.values()]

    def draw_bar(self, current_amount, max_amount, bg_rect, color):
        """
        Draw a colored bar representing a statistic.

        Args:
            current_amount (int): The current value of the statistic.
            max_amount (int): The maximum value of the statistic.
            bg_rect (pygame.Rect): The background rectangle of the bar.
            color (str): The color of the bar.

        Returns:
            None

        """
        # Draw background
        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Convert stat to pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Draw bar
        pg.draw.rect(self.display_surface, color, current_rect)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def draw_xp(self, experience):
        """
        Draw the player's experience points.

        Args:
            experience (float): The player's current experience points.

        Returns:
            None

        """
        text_surface = self.font.render(str(int(experience)), False, TEXT_COLOR)
        x, y = self.display_surface.get_size()
        x -= 20
        y -= 20
        text_rect = text_surface.get_rect(bottomright=(x, y))

        rect_inflate = text_rect.inflate(20, 20)
        pg.draw.rect(self.display_surface, UI_BG_COLOR, rect_inflate)
        pg.draw.rect(self.display_surface, UI_BORDER_COLOR, rect_inflate, 3)
        self.display_surface.blit(text_surface, text_rect)

    def draw_selection_box(self, left, top, has_switched):
        """
        Draw a selection box with optional highlighting.

        Args:
            left (int): The left position of the selection box.
            top (int): The top position of the selection box.
            has_switched (bool): True if the selection has switched; False otherwise.

        Returns:
            pygame.Rect: The rectangle of the selection box.

        """
        bg_rect = pg.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        border_color = UI_BORDER_COLOR_ACTIVE if has_switched else UI_BORDER_COLOR

        pg.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pg.draw.rect(self.display_surface, border_color, bg_rect, 3)

        return bg_rect

    def overlay(self, images, index, left, top, has_switched):
        """
        Overlay an image on top of a selection box.

        Args:
            images (list): A list of images to overlay.
            index (int): The index of the image to overlay.
            left (int): The left position of the selection box.
            top (int): The top position of the selection box.
            has_switched (bool): True if the selection has switched; False otherwise.

        Returns:
            None

        """
        bg_rect = self.draw_selection_box(left, top, has_switched)
        image = images[index]
        image_rect = image.get_rect(center=bg_rect.center)

        self.display_surface.blit(image, image_rect)

    def weapon_overlay(self, weapon_index, has_switched):
        """
        Overlay a weapon image on a selection box.

        Args:
            weapon_index (int): The index of the weapon image to overlay.
            has_switched (bool): True if the selection has switched; False otherwise.

        Returns:
            None

        """
        self.overlay(self.weapon_graphics, weapon_index, 10, 630, has_switched)

    def magic_overlay(self, magic_index, has_switched):
        """
        Overlay a magic style image on a selection box.

        Args:
            magic_index (int): The index of the magic style image to overlay.
            has_switched (bool): True if the selection has switched; False otherwise.

        Returns:
            None

        """
        self.overlay(self.magic_graphics, magic_index, 80, 635, has_switched)

    def display(self, player):
        """
        Display the UI elements for the player.

        Args:
            player (Player): The player object containing relevant statistics.

        Returns:
            None

        """
        self.draw_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.draw_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)
        self.draw_xp(player.experience)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
