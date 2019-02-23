"""Convienience wrapper around pkg_resources"""

import pkg_resources

def stream(filename):
    return pkg_resources.resource_stream('ascended_tracking.resources', filename)

def path(filename):
    return pkg_resources.resource_filename('ascended_tracking.resources', filename)

def get(filename):
    return pkg_resources.resource_string('ascended_tracking.resources', filename)
