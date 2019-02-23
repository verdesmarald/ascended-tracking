"""This panel displays a summary of the runs in the current session."""
import time

import wx

from ascended_tracking import run, parser, watcher
from ascended_tracking.gui import app

class CurrentSessionPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self._session = {}
        self._watcher = watcher.watch(app.STATS_LOCATION, self._on_create, False)
        self._text = wx.StaticText(self, label=self._get_summary())

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self._text, wx.ID_ANY, wx.EXPAND | wx.ALL)
        self.SetSizer(vbox)


    def _on_create(self, event):
        if not parser.is_stats_file(event.src_path):
            return

        time.sleep(1)

        stats = run.Run(event.src_path)
        self._session.setdefault(stats.name, []).append(stats)
        self._text.SetLabel(self._get_summary())


    def _get_summary(self):
        _lines = [f'{_name}, {len(_runs)}' for _name, _runs in self._session.items()]
        _lines.sort()

        return '\n'.join(_lines)
