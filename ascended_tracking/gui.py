# -*- coding: utf-8 -*-

"""GUI entry point."""

import collections
import os
from time import sleep

import wx
from watchdog.events import FileSystemEventHandler

from ascended_tracking import parser
from ascended_tracking.watcher import Watcher
from ascended_tracking.run import Run

STATS_LOCATION = 'F:/Games/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/stats'

def read_stats():
    for fname in os.listdir(STATS_LOCATION):
        _path = os.path.join(STATS_LOCATION, fname)

        if not parser.is_stats_file(_path):
            continue

        yield Run(_path)



class StatsFileCreatedHandler(FileSystemEventHandler):
    """Handler for watchdog events that are triggered when a stats
    file is created.
    """
    _MAX_ATTEMPTS = 3

    def __init__(self):
        super().__init__()
        self.counter = collections.Counter()

    def on_created(self, event):
        if not parser.is_stats_file(event.src_path):
            return

        _attempt = 1
        while True:
            sleep(1)
            try:
                # This call reads the stats file and can fail if
                # FPS Aim Trainer hasn't release the write handle yet.
                _stats = parser.parse_stats(event.src_path)
                break
            except PermissionError:
                if _attempt == self._MAX_ATTEMPTS:
                    raise

        _name = _stats['name']
        self.counter[_name] += 1
        print(_name, self.counter[_name], _stats['summary']['Score'])


def main():
    for run in read_stats():
        #print(f'{run.timestamp} {run.name} {run.weapons[0].accuracy() * 100:.2f}% {run.score:.2f} ({run.hash})')
        print(f'"{run.timestamp}","{run.name}",{run.weapons[0].accuracy():.2f},{run.score:.2f}')

    Watcher().watch(STATS_LOCATION, StatsFileCreatedHandler())

    _app = wx.App()

    _frame = wx.Frame(None, title='Ascended Tracking')
    _frame.Centre()
    _frame.Show()

    _app.MainLoop()
