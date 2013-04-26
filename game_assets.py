from copy import copy
import os
import random

from pygame import display, Surface

from const import MAPS_DIR, CONFIG_DIR, MUSIC_DIR
from asset_loaders import Asset, LoadableAsset, load_image, load_font
from utils import get_color, word_wrap


class Config(LoadableAsset):

    path = CONFIG_DIR
    location = 'config.json'
    schema = [{
        'screen': [
            'title',
            'width',
            'height',
            'tile_width',
            'tile_height',
            'map_display_width',
            'map_display_height',
        ]},
        'start',
        'images',
        'fonts',
        'music',
        'score_font',
        'raspberries_font', {
            'dialog_box': [
                'x', 'y', 'char_width', 'char_height'
            ]
        },
        {'keypress_repeat': [
            'delay',
            'interval'
            ]
        }
    ]

    def handle(self, data):
        super(Config, self).handle(data)
        self.images = dict(map(load_image, self.images))
        self.fonts = dict(map(load_font, self.fonts))
        self.music = os.path.join(MUSIC_DIR, self.music) if self.music else ''
        self.screen['map_display_mid_x'] = self.screen['map_display_width'] / 2
        self.screen['map_display_mid_y'] = self.screen['map_display_height'] / 2
        self.questions = Questions(
            self.questions, width=self.dialog_box['char_width']
        )


class Questions(LoadableAsset):
    path = CONFIG_DIR
    schema = {
        'questions': [
            'question',
            'answers',
            'correct',
        ]
    }

    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', 20)
        super(Questions, self).__init__(*args, **kwargs)
        self.next()

    def next(self):
        self.current_index = random.choice(range(len(self.questions)))
        self.current_question = self.questions[self.current_index]
        self.choice = 0
        self._question_display = None

    def handle(self, data):
        super(Questions, self).handle(data)
        self.question_displays = [
            word_wrap(question['question'], self.width)
            for question in self.questions
        ]

    def get_choices_length(self):
        return len(self.current_question['answers'])

    def get_question_display(self):
        question_display = copy(self.question_displays[self.current_index])
        question_display.append('')
        for index, answer in enumerate(self.current_question['answers']):
            prefix = '[X]' if index == self.choice else '[ ]'
            question_display.append(' '.join((prefix, answer)))
        return question_display

    def is_correct(self):
        return self.choice == self.current_question['correct']


class Screen(Asset):

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self._create_context()

    def _create_context(self):
        display.set_caption(self.title)
        self.context = display.set_mode((self.width, self.height))

    def set_background(self, color=''):
        color = color or 'black'
        background = Surface(self.context.get_size()).convert()
        background.fill(get_color(color))
        self.background = background


class Map(Asset):

    def handle(self, data):
        super(Map, self).handle(data)
        self.tile_solids = [tile in self.solids for tile in self.tiles]
        self.images = dict(map(load_image, self.legend.values()))

    def get_index(self, x, y):
        return y * self.dimensions['width'] + x


class Item(Asset):
    pass


class Mob(Asset):
    x = 0
    y = 0
    items = []


class Player(Mob):
    raspberries = 0


class Level(LoadableAsset):

    path = MAPS_DIR
    schema = {
        'map': [
            'solids',
            'legend',
            'tiles',
            {
                'dimensions': [
                    'width', 'height'
                ],
            },
            {
                'player_start': [
                    'x', 'y'
                ],
            }
        ],
    }

    def clean_map(self, map_data):
        player_start = map_data['player_start']
        x, y = player_start['x'], player_start['y']
        dimensions = map_data['dimensions']
        num_tiles = dimensions['width'] * dimensions['height']
        if len(map_data['tiles']) != num_tiles:
            self.error = u'Number of tiles must equal width * height'
            return False
        if x < 0 or y < 0 or x >= dimensions['width'] or y >= dimensions['height']:
            self.error = u'The player_start x or y is out of bounds'
            return False
        return True

    def handle(self, data):
        self.map = Map(data['map'])
