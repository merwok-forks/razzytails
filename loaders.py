#!usr/bin/env python
from random import shuffle

import pygame

from game_assets import Config, Level, Screen, Player


def initialize():
    """
    Initializes pygame, loads the configuration file and creates a display
    context. Returns a 3-item tuple in the form of: (config, screen, player)
    """
    pygame.init()
    pygame.mixer.init()
    config = Config()
    screen = Screen(config.screen)
    screen.set_background('black')
    player = Player()
    return screen, config, player


def load_map(map_filename, player):
    level = Level(map_filename)
    # TODO: Remove once items are added
    # Create and attach raspberry coordinates.
    width, height = level.map.dimensions['width'], level.map.dimensions['height']
    raspberry_coordinates = []
    for y in xrange(height):
        for x in xrange(width):
            if not level.map.tile_solids[level.map.get_index(x, y)]:
                raspberry_coordinates.append((x, y))
    shuffle(raspberry_coordinates)
    level.map.raspberry_coordinates = raspberry_coordinates[:10]
    # Place player at the start location
    player.x = level.map.player_start['x']
    player.y = level.map.player_start['y']
    return level
