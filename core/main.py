import pygame as pg
from .settings import *
from .level import Level

class Game:
    """
    Represents the main game controller for the "TerraMythica" game.

    Attributes:
        screen (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The clock object for controlling frame rate.
        level (Level): The game level object.
        run (bool): Flag to control the game's main loop.

    Methods:
        __init__(self):
            Initialize a Game instance and set up the game window and resources.
        initialize(self):
            Perform one-time initialization tasks.
        handle_events(self):
            Handle user input events.
        run_game(self):
            Start the main game loop to run the game.
    """

    def __init__(self) -> None:
        """
        Initialize a Game instance.

        Returns:
            None
        """
        pg.init()
        icon = pg.image.load(WINDOW_ICON)
        pg.display.set_icon(icon)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("TerraMythica")
        self.clock = pg.time.Clock()
        self.level = Level()
        self.run = True

    def initialize(self):
        """
        Perform one-time initialization tasks.

        - Loads and plays the main music.
        
        Returns:
            None
        """
        main_music = pg.mixer.Sound(MAIN_MUSIC)
        main_music.set_volume(0.1)
        main_music.play(loops=-1)

    def handle_events(self):
        """
        Handle user input events.

        - Monitors user input events, such as quitting the game or toggling the upgrade menu.

        Returns:
            None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self.level.toggle_menu()

    def run_game(self):
        """
        Start the main game loop to run the game.

        - Clears the game screen with the background color.
        - Updates and runs the game level.
        - Updates the display.
        - Controls the frame rate.

        Returns:
            None
        """
        self.initialize()

        while self.run:
            self.handle_events()
            
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pg.display.update()
            self.clock.tick(FPS)
