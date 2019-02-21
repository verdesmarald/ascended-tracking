"""Simple file system watcher to monitor the stats folder and fire and
event when a new file is created.
"""

from watchdog.observers import Observer


class Watcher(object):
    def __init__(self):
        self.observer = Observer()

    def watch(self, directory, callback):
        self.observer.schedule(callback, directory, recursive=True)
        self.observer.start()
        return self.observer
