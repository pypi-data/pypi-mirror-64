#!/usr/bin/env python
import os
import public

"""
import django_find_apps

INSTALLED_APPS = django_find_apps.find_apps(".") + [
    ...
]
"""

APPS_FILES = [
    'admin.py',
    'apps.py',
    'models.py',
]
APPS_DIRS = [
    'admin',
    'apps',
    'models',
    'management/commands',
    'templatetags'
]

def isapp(path):
    if not os.path.exists(os.path.join(path, '__init__.py')):
        return False
    for app_file in APPS_FILES:
        fullpath = os.path.join(path, app_file)
        if os.path.exists(fullpath) and os.path.isfile(fullpath):
            return True
    for app_dir in APPS_DIRS:
        fullpath = os.path.join(path, app_dir)
        if os.path.exists(fullpath) and os.path.isdir(fullpath):
            return True

def find_package_dirs(path):
    for root, dirs, files in os.walk(path):
        _dirs = dirs[:]
        dirs = []
        for _dir in _dirs:
            fullpath = os.path.join(root, _dir)
            if isapp(fullpath):
                yield fullpath
                dirs.append(_dir)

@public.add
def find_apps(path):
    """return a list of apps"""
    if not path:
        raise ValueError('invalid path: %s' % path)
    if path and path[0]=='/':
        raise ValueError('absolute path not allowed: %s' % path)
    apps = []
    for _dir in filter(isapp,find_package_dirs(path)):
        relpath = os.path.relpath(_dir, path)
        if path in ['.','./']:
            apps.append(relpath.replace(os.path.sep, '.'))
        else:
            apps.append(path+'.'+relpath.replace(os.path.sep, '.'))
    return apps
