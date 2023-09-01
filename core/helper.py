from csv import reader
from pathlib import Path
from os import walk
import pygame as pg


def import_csv_layout(path):
    """
    Import a CSV layout from a given file path.

    Args:
        path (str or pathlib.Path): The path to the CSV file containing the layout.

    Returns:
        list of list: A 2D list representing the layout read from the CSV file.
    """
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        return [list(row) for row in layout]

def import_folder(path):
    """
    Import images from a folder.

    Args:
        path (str or pathlib.Path): The path to the folder containing image files.

    Returns:
        list of pygame.Surface: A list of pygame image surfaces loaded from the image files in the folder.
    """
    return [
        pg.image.load(Path.joinpath(path, image)).convert_alpha()
        for _, __, image_files in walk(path)
        for image in image_files
    ]
