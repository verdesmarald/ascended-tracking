from ascended_tracking import parser


class Run(object):
    def __init__(self, path, load_details=False):
        self.path = path
        self.name, self.mode, self.timestamp = parser.parse_filename(path)

        self.raw = None
        self.hash = None
        self.weapons = None
        self.score = None
        self.details_loaded = False

        if load_details:
            self.load_details()

    def load_details(self):
        if self.details_loaded:
            return

        _raw = parser.parse_stats(self.path)
        self.raw = _raw
        self.hash = _raw['hash']
        self.weapons = [Weapon(weapon) for weapon in _raw['weapons']]
        self.score = float(_raw['summary']['Score'])
        self.details_loaded = True


class Weapon(object):
    def __init__(self, _raw):
        self.name = _raw['Weapon']
        self.shots = int(_raw['Shots'])
        self.hits = int(_raw['Hits'])

    def accuracy(self):
        if self.shots == 0:
            return 0

        return self.hits / self.shots
