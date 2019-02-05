from fysom import *

fsm = Fysom({'initial': 'awake',
             'final': 'end',
             'events': [
                 {'name': 'wakeup', 'src': 'sleeping', 'dst': 'awake'},
                 {'na.me': 'sleep', 'src': 'awake', 'dst': 'sleeping'}]})