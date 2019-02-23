"""Simple file system watcher to monitor the stats folder and fire and
event when a new file is created.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class _CreateHandler(FileSystemEventHandler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler

    def on_created(self, event):
        self.handler(event)


def watch(directory, on_created, recursive):
    observer = Observer()
    observer.schedule(_CreateHandler(on_created), directory, recursive=recursive)
    observer.start()
    return observer
