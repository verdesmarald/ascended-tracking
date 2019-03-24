class Session(object):
    def __init__(self):
        self.start = None
        self.end = None
        self.scenarios = {}

    def add_run(self, run):
        if run.details_loaded and run.score == 0:
            # When a run is exited early via the "Restart Challenge" or
            # "Cancel Challenge" menu item it is still recoreded with a
            # score of 0, but shouldn't be included in the session.
            return

        if not self.start or run.timestamp < self.start:
            self.start = run.timestamp

        if not self.end or run.timestamp > self.end:
            self.end = run.timestamp

        self.scenarios.setdefault(run.name, []).append(run)

    def clear(self):
        self.scenarios = {}

    def load_details(self):
        for _scenario, _runs in self.scenarios.items():
            for _run in _runs:
                _run.load_details()

            _runs[:] = [_run for _run in _runs if _run.score != 0]
