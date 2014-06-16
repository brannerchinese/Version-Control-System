#! /usr/bin/env python
# myvcs.py
# David Prager Branner
# 20140615

import sys
if sys.version_info.major < 3 and sys.version_info.minor < 3:
    print('At least Python 3.3 is required to run this program.')
    sys.exit(0)
import difflib as D
import os
import argparse
import shutil

myvcs_ignore = {'.myvcs', '.myvcs.py.swp', '__pycache__', 'myvcs.py'}

def main(args=None):
    actions = {
            'checkout': checkout,
            'latest': checkout,
            'backup': copy_files,
            }
    if not args:
        copy_files()
    else:
        try:
            actions[args[0]](args[1:])
        except KeyError:
            print('Command-line argument {} not found; exiting.'.
                    format(args[0]))

def checkout(snapshot=None):
    if not snapshot:
        # Get and check out highest-numbered snapshot.
        snapshot = get_highest_snapshot()
    else:
        snapshot = int(snapshot[0])
    print('snapshot: {}'.format(snapshot))
    # First back up current version of current_dir.
    copy_files()
    # Then replace it with desired snapshot (if it exists).
    source = os.path.join('.myvcs', str(snapshot))
    print('source:', source)
    if os.path.exists(source):
        print('here')
        copy_files(source=source, destination='current_dir')
    else:
        print('Snapshot {} does not exist; exiting.')
        sys.exit()

def latest(args):
    checkout()

def get_highest_snapshot():
    if not os.path.exists('.myvcs'):
        print('Subdirectory .myvcs not found; exiting.')
        sys.exit()
    else:
        # Use loop rather than comprehension so as to allow try-block.
        catalog = []
        for i in os.listdir('.myvcs'):
            try:
                catalog.append(int(i))
            except ValueError:
                continue
        catalog.sort()
#        print('catalog: {}'.format(catalog))
        return catalog[-1]


def copy_files(args=None, source=None, destination=None):
    if not source:
        source = 'current_dir'
        if not os.path.exists('current_dir'):
            print('Directory current_dir does not exist; exiting')
            sys.exit()
    print('source:', source)
    # Get last backup dir and create directory for next backups, if needed.
    if not destination:
        destination = os.path.join('.myvcs', get_working_mvc_dir())
    print('destination:', destination)
    # Copy whole directory.
    if os.path.exists(destination):
        shutil.rmtree(destination)
    x = shutil.copytree(source, destination)
    print('Done backing up current directory.\n')

def get_working_mvc_dir():
    # QQQ This should happen only on initialization.
    if '.myvcs' not in os.listdir():
        os.mkdir('.myvcs')
        head = -1
    else:
        # Read .myvcs/HEAD and make sure that directory exists.
        if os.path.exists(os.path.join('.myvcs', 'HEAD')):
            with open(os.path.join('.myvcs', 'HEAD'), 'r') as f:
                head = int(f.read())
        if not (os.path.exists(os.path.join('.myvcs', str(head))) or
                os.path.isdir(os.path.join('.myvcs', str(head)))):
            print('Invalid value of .myvcs/HEAD: {}'.format(head))
    # Set HEAD to new working directory.
    head += 1
    with open(os.path.join('.myvcs', 'HEAD'), 'w') as f:
        f.write(str(head))
    return str(head)

def defunct():
    # Get list of all files in present directory.
    directories = collections.deque([current_dir])
    while directories:
        next_dir = directories.popleft()
        print('\nnow doing', next_dir)
        all_files = os.listdir(next_dir)
        print(directories, all_files)
        for f in all_files:
            if f in myvcs_ignore:
                continue
            print('\nfile:    {}'.format(f))
            full_path = os.path.normpath(os.path.join(next_dir, f))
            print('file:    {}'.
                    format(full_path))
            if os.path.isdir(full_path):
                print('new directory:', f)
                directories.append(full_path)
                print(directories, all_files)

if __name__ == '__main__':
    main(sys.argv[1:])

