# -*- coding: utf-8 -*-

"""GUI entry point."""

import collections
import os
from datetime import datetime, timedelta
from time import sleep

import wx
from watchdog.events import FileSystemEventHandler

from ascended_tracking import parser, resource, watcher
from ascended_tracking.gui import panels
from ascended_tracking.run import Run
from ascended_tracking.session import Session

STATS_LOCATION = 'F:/Games/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/stats'

def read_stats(load_details):
    for fname in os.listdir(STATS_LOCATION):
        _path = os.path.join(STATS_LOCATION, fname)

        if not parser.is_stats_file(_path):
            continue

        yield Run(_path, load_details=load_details)


def get_sessions():
    _runs = list(read_stats(False))
    _runs.sort(key=lambda _run: _run.timestamp)

    _current_session = Session()
    _sessions = [_current_session]
    _max_gap = timedelta(hours = 1)

    for _run in _runs:
        if _current_session.end and _run.timestamp - _current_session.end > _max_gap:
            _current_session = Session()
            _sessions.append(_current_session)
        _current_session.add_run(_run)

    return _sessions


def main():
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except:
        pass

    _sessions = get_sessions()
    _cutoff = datetime.now() - timedelta(hours = 1)

    _current_session = _previous_session = None
    if _sessions:
        if _sessions[-1].end > _cutoff:
            _current_session = _sessions[-1]
            if len(_sessions) > 1:
                _previous_session = _sessions[-6]
        else:
            _previous_session = _sessions[-1]

    for _session in _sessions:
        print(f'{_session.start} {_session.end} {len(_session.scenarios)} {sum([len(_runs) for _, _runs in _session.scenarios.items()])}')

    _app = wx.App()

    _frame = wx.Frame(None, title='Ascended Tracking', size=(1200, 900))
    _panel = panels.CurrentSessionPanel(_frame, session=_current_session, previous_session=_previous_session)

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
