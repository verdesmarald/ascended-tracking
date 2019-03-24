"""This panel displays a summary of the runs in the current session."""
import time

import wx

from ascended_tracking import run, parser, watcher
from ascended_tracking.session import Session
from ascended_tracking.gui import app

class SessionPanel(wx.Panel):
    """Displays information about an FPS Aim Trainer session."""
    def __init__(self, parent, session=None, previous_session=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._session = session or Session()
        self._previous_session = previous_session
        self._init_ui()

    def _init_ui(self):
        self._summary = wx.ListCtrl(self, style=(wx.LC_REPORT | wx.LC_SINGLE_SEL))

        for _col in [
            ('Scenario', 300), ('Count', 150),
            ('Accuracy', 150), ('Score', 150),
            ('Prev Acc.', 150), ('Prev Score', 150)
        ]:
            self._summary.AppendColumn(_col[0], width=_col[1])

        _hbox = wx.BoxSizer(wx.HORIZONTAL)
        _hbox.Add(self._summary, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(_hbox)

        self.refresh()

    def add(self, run):
        self._session.add_run(run)

    def refresh(self):
        self._summary.DeleteAllItems()

        for _name, _runs in self._session.scenarios.items():
            _avg_accuracy = self._get_accuracy(_runs)
            _avg_score = self._get_score(_runs)

            _prev_accuracy = _prev_score = 0
            if self._previous_session and _name in self._previous_session.scenarios:
                _prev_runs = self._previous_session.scenarios[_name]
                _prev_accuracy = self._get_accuracy(_prev_runs)
                _prev_score = self._get_score(_prev_runs)

            row = (
                _name,
                len(_runs),
                f'{_avg_accuracy * 100:.2f}%',
                f'{_avg_score:.2f}',
                f'{_prev_accuracy * 100:.2f}%',
                f'{_prev_score:.2f}'
            )
            self._summary.Append(row)

    def _get_accuracy(self, runs):
        return sum([_run.weapons[0].accuracy() for _run in runs if _run.details_loaded]) / len(runs)

    def _get_score(self, runs):
        return sum([_run.score for _run in runs if _run.details_loaded]) / len(runs)


class CurrentSessionPanel(SessionPanel):
    def __init__(self, parent, session=None, previous_session=None):
        if session:
            session.load_details()

        if previous_session:
            previous_session.load_details()

        super().__init__(parent, session=session, previous_session=previous_session)
        self._watcher = watcher.watch(app.STATS_LOCATION, self._on_create, False)

    def _on_create(self, event):
        if not parser.is_stats_file(event.src_path):
            return

        time.sleep(1)
        _run = run.Run(event.src_path, load_details=True)
        self.add(_run)
        self.refresh()
