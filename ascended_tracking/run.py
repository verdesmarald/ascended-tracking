from ascended_tracking import parser


class Run(object):
    def __init__(self, path):
        _raw = parser.parse_stats(path)
        self.raw = _raw

        self.name = _raw['name']
        self.mode = _raw['mode']
        self.timestamp = _raw['timestamp']
        self.hash = _raw['hash']

        self.weapons = [Weapon(weapon) for weapon in _raw['weapons']]
        self.score = float(_raw['summary']['Score'])


class Weapon(object):
    def __init__(self, _raw):
        self.name = _raw['Weapon']
        self.shots = int(_raw['Shots'])
        self.hits = int(_raw['Hits'])

    def accuracy(self):
        if self.shots == 0:
            return 0

        return self.hits / self.shots
