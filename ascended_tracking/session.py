class Session(object):
    def __init__(self):
        self.scenarios = {}

    def add_run(self, run):
        if run.score == 0:
            # When a run is exited early via the "Restart Challenge" or
            # "Cancel Challenge" menu item it is still recoreded with a
            # score of 0, but shouldn't be included in the session.
            return

        self.scenarios.setdefault(run.name, []).append(run)

    def clear(self):
        self.scenarios = {}

    def load_details(self):
        for _scenario, _runs in self.scenarios.items():
            for _run in _runs:
                _run.load_details()
