# -*- coding: utf-8 -*-

"""GUI entry point."""

import collections
import os
from time import sleep

import wx
from watchdog.events import FileSystemEventHandler

from ascended_tracking import parser, resource, watcher
from ascended_tracking.gui import panels
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
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    #for run in read_stats():
        #print(f'{run.timestamp} {run.name} {run.weapons[0].accuracy() * 100:.2f}% {run.score:.2f} ({run.hash})')
        #print(f'"{run.timestamp}","{run.name}",{run.weapons[0].accuracy():.2f},{run.score:.2f}')

    #watcher.watch(STATS_LOCATION, StatsFileCreatedHandler())

    _app = wx.App()

    _frame = wx.Frame(None, title='Ascended Tracking', size=(1200, 900))
    _panel = panels.CurrentSessionPanel(_frame)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
    _frame.SetSizer(vbox)

    _frame.Centre()
    _frame.Show()
    _toolbar = _get_toolbar(_frame)
    _frame.SetToolBar(_toolbar)
    _toolbar.Realize()

    _app.MainLoop()


def _get_toolbar(parent):
    _toolbar = wx.ToolBar(parent, style=(wx.TB_TEXT|wx.TB_NODIVIDER))
    _icon = wx.Bitmap(resource.path('current.png'))
    _toolbar.AddTool(wx.ID_ANY, 'Current Session', _icon)
    return _toolbar
