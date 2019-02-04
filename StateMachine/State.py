from fysom import *

fsm = Fysom({'initial': 'awake',
             'final': 'red',
             'events': [
                 {'name': 'wakeup', 'src': 'sleeping', 'dst': 'awake'},
                 {'name': 'sleep', 'src': 'awake', 'dst': 'sleeping'}]})