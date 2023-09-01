import pygame as pg
from .settings import *


class Upgrade:
    """
    Represents the player's upgrade menu.

    Attributes:
        display_surface (pygame.Surface): The display surface.
        player (Player): The player object.
        attribute_number (int): The number of attributes the player can upgrade.
        attribute_names (list): The names of the attributes.
        max_values (list): The maximum values of the attributes.
        font (pygame.font.Font): The font for UI text.
        height (int): The height of the upgrade menu.
        width (int): The width of each upgrade item.
        items_list (list): A list of upgrade items.
        selection_index (int): The index of the currently selected upgrade item.
        selection_time (int): The time when the last selection was made.
        cooldown_time (int): The cooldown time for selection.
        can_move (bool): Indicates whether the player can move the selection.

    Methods:
        input():
            Handles user input for navigating and selecting upgrades.

        selection_cooldown():
            Manages the cooldown time between selections.

        create_items():
            Creates the list of upgrade items.

        display():
            Displays the upgrade menu and items.

    """

    def __init__(self, player) -> None:
        """
        Initialize an Upgrade menu.

        Args:
            player (Player): The player object.

        Returns:
            None

        """
        self.display_surface = pg.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pg.font.Font(UI_FONT, UI_FONT_SIZE)

        # Item dimensions:
        # Multiply "y" by 0.8 to get a 20% offset
        self.height = self.display_surface.get_size()[1] * 0.8

        # Divide "x" by 6 (attribute_number + 1) for padding between items
        self.width = self.display_surface.get_size()[0] // 6

        self.create_items()

        # Selection system
        self.selection_index = 0
        self.selection_time = None
        self.cooldown_time = 300
        self.can_move = True

    def input(self):
        """
        Handles user input for navigating and selecting upgrades.

        Returns:
            None

        """
        keys = pg.key.get_pressed()
        if self.can_move:
            if keys[pg.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pg.time.get_ticks()
            elif keys[pg.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pg.time.get_ticks()

            if keys[pg.K_SPACE]:
                self.can_move = False
                self.selection_time = pg.time.get_ticks()
                self.items_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        """
        Manages the cooldown time between selections.

        Returns:
            None

        """
        if not self.can_move:
            current_time = pg.time.get_ticks()
            if current_time - self.selection_time >= self.cooldown_time:
                self.can_move = True

    def create_items(self):
        """
        Creates the list of upgrade items.

        Returns:
            None

        """
        self.items_list = []

        for item, index in enumerate(range(self.attribute_number)):
            # Vertical position
            top = self.display_surface.get_size()[1] * 0.1

            # Horizontal position
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            item = Item(left, top, self.width, self.height, index, self.font)
            self.items_list.append(item)

    def display(self):
        """
        Displays the upgrade menu and items.

        Returns:
            None

        """
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.items_list):
            # Get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    """
    Represents an individual upgrade item.

    Attributes:
        rect (pygame.Rect): The rectangular bounds of the upgrade item.
        index (int): The index of the upgrade item.
        font (pygame.font.Font): The font for UI text.

    Methods:
        display_names(surface, name, cost, selected):
            Displays the upgrade item's name and cost.

        display_bar(surface, value, max_value, selected):
            Displays the upgrade item's progress bar.

        trigger(player):
            Triggers the upgrade for the player.

        display(surface, selection_number, name, value, max_value, cost):
            Displays the upgrade item.

    """

    def __init__(self, left, top, width, height, index, font) -> None:
        """
        Initialize an Item.

        Args:
            left (int): The left coordinate of the item.
            top (int): The top coordinate of the item.
            width (int): The width of the item.
            height (int): The height of the item.
            index (int): The index of the item.
            font (pygame.font.Font): The font for UI text.

        Returns:
            None

        """
        self.rect = pg.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        """
        Displays the upgrade item's name and cost.

        Args:
            surface (pygame.Surface): The display surface.
            name (str): The name of the upgrade item.
            cost (float): The cost of the upgrade.
            selected (bool): Indicates whether the item is selected.

        Returns:
            None

        """
        # Selection highlight
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # Title
        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(midtop=self.rect.midtop + pg.math.Vector2(0, 20))

        # Cost
        cost = str(int(cost))
        cost_surface = self.font.render(cost, False, color)
        cost_rect = cost_surface.get_rect(midbottom=self.rect.midbottom - pg.math.Vector2(0, 20))

        # Draw
        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        """
        Displays the upgrade item's progress bar.

        Args:
            surface (pygame.Surface): The display surface.
            value (float): The current value of the attribute being upgraded.
            max_value (float): The maximum value of the attribute.
            selected (bool): Indicates whether the item is selected.

        Returns:
            None

        """
        top = self.rect.midtop + pg.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pg.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # Calculate progress bar size and growth
        full_height = bottom[1] - top[1]
        relative_numer = (value / max_value) * full_height
        value_rect = pg.Rect(top[0] - 15, bottom[1] - relative_numer, 30, 10)

        pg.draw.line(surface, color, top, bottom, 5)
        pg.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        """
        Triggers the upgrade for the player.

        Args:
            player (Player): The player object.

        Returns:
            None

        """
        upgrade_attribute = list(player.stats.keys())[self.index]

        if (
            player.experience >= player.upgrade_cost[upgrade_attribute]
            and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]
        ):
            player.experience -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_number, name, value, max_value, cost):
        """
        Displays the upgrade item.

        Args:
            surface (pygame.Surface): The display surface.
            selection_number (int): The index of the selected upgrade item.
            name (str): The name of the upgrade item.
            value (float): The current value of the attribute being upgraded.
            max_value (float): The maximum value of the attribute.
            cost (float): The cost of the upgrade.

        Returns:
            None

        """
        if self.index == selection_number:
            pg.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pg.draw.rect(surface, UI_BG_COLOR, self.rect)
            pg.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_number)
        self.display_bar(surface, value, max_value, self.index == selection_number)
