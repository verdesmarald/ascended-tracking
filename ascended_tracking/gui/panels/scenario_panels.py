"""This panel displays a summary of the runs in the current session."""
import time

import wx

from ascended_tracking import run, parser, watcher
from ascended_tracking.gui import app

class SessionPanel(wx.Panel):
    """Displays information about an FPS Aim Trainer session."""
    def __init__(self, parent, session, **kwargs):
        super().__init__(parent, **kwargs)
        self._session = session
        self._init_ui()

    def _init_ui(self):
        self._summary = wx.ListCtrl(self, style=(wx.LC_REPORT | wx.LC_SINGLE_SEL))

        for _col in [('Scenario', 300), ('Count', 150), ('Accuracy', 150), ('Score', 150)]:
            self._summary.AppendColumn(_col[0], width=_col[1])

        _hbox = wx.BoxSizer(wx.HORIZONTAL)
        _hbox.Add(self._summary, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(_hbox)

        self.refresh()

    def refresh(self):
        self._summary.DeleteAllItems()

        for _name, _runs in self._session.items():
            _avg_accuracy = sum([_run.weapons[0].accuracy() for _run in _runs]) / len(_runs)
            _avg_score = sum([_run.score for _run in _runs]) / len(_runs)
            row = (
                _name,
                len(_runs),
                f'{_avg_accuracy * 100:.2f}%',
                f'{_avg_score:.2f}'
            )
            self._summary.Append(row)


class CurrentSessionPanel(SessionPanel):
    def __init__(self, parent):
        super().__init__(parent, {})
        self._watcher = watcher.watch(app.STATS_LOCATION, self._on_create, False)
        self._session = {}

    def _on_create(self, event):
        if not parser.is_stats_file(event.src_path):
            return

        time.sleep(1)
        stats = run.Run(event.src_path)
        self._session.setdefault(stats.name, []).append(stats)
        self.refresh()
