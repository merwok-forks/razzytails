"""Defines transitions and callbacks for the game's fsm"""

from fsm import FSM
from dispatch import Dispatch


# FSM transitions and callbacks
transitions = [
    {
        'name': 'answer',
        'source': 'dialog',
        'destination': 'main',
    },
    {
        'name': 'popup',
        'source': 'main',
        'destination': 'dialog'
    },
    {
        'name': 'exit',
        'source': 'main',
        'destination': 'exit'
    },
    {
        'name': 'exit',
        'source': 'dialog',
        'destination': 'exit'
    },
    {
        'name': 'start',
        'source': 'splash',
        'destination': 'main'
    }
]

# No callbacks for now. Refer to fsm.py when implementating
callbacks = {}

game_state = FSM('splash', transitions, callbacks)
