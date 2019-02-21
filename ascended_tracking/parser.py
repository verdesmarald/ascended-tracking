"""Methods for parsing .csv stats files from FPS Aim Trainer."""

import csv
import hashlib
import os
import re

from datetime import datetime

STATS_FILE_REGEX = re.compile(r'^(.*) - (\w+) - (\d{4}.\d\d.\d\d-\d\d.\d\d.\d\d) Stats.csv$')

def is_stats_file(path):
    """Checks if the given path points to a valid stats file."""
    return STATS_FILE_REGEX.match(path) is not None


def parse_stats(path):
    """Parse the stats from the stats file pointed to by path."""
    _fname = os.path.basename(path)
    _match = STATS_FILE_REGEX.match(_fname)

    if not _match:
        raise TypeError(f'{path} is not a valid stats file')

    _name, _mode, _timestr = _match.groups()

    with open(path) as stats_file:
        _content = stats_file.read()
        _hash = hashlib.sha1(_content.encode('utf-8')).hexdigest()
        parts = [part.splitlines() for part in _content.split('\n\n')]

    if len(parts) != 4:
        raise TypeError(f'{path} is not a valid stats file')

    return {
        'name': _name,
        'mode': _mode,
        'timestamp': datetime.strptime(_timestr, '%Y.%m.%d-%H.%M.%S'),
        'hash': _hash,
        'kills': list(csv.DictReader(parts[0])),
        'weapons': list(csv.DictReader(parts[1])),
        'summary': {f[0][:-1] : f[1] for f in csv.reader(parts[2])},
        'settings': {f[0][:-1] : f[1] for f in csv.reader(parts[3])}
    }
