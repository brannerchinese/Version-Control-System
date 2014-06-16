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
            'current': print_current_head,
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
    """Copy a given snapshot into current_dir."""
    if not snapshot:
        # Get and check out highest-numbered snapshot.
        snapshot = get_highest_snapshot()
    else:
        snapshot = int(snapshot[0])
    # Then replace it with desired snapshot (if it exists).
    source = os.path.join('.myvcs', str(snapshot))
    if os.path.exists(source):
        copy_files(source=source, destination='current_dir', snapshot=snapshot)
        print('Checked out snapshot {}.'.format(snapshot))
    else:
        print('Snapshot {} does not exist; exiting.'.format(snapshot))
        sys.exit()

def latest(args):
    """Copy current snapshot into current_dir."""
    checkout()

def get_highest_snapshot():
    """Find number of highest-numbered snapshot; return as int."""
    if not os.path.exists('.myvcs'):
        os.mkdir('.myvcs')
        return -1
    else:
        # Use loop rather than comprehension so as to allow try-block.
        catalog = []
        for i in os.listdir('.myvcs'):
            try:
                catalog.append(int(i))
            except ValueError:
                continue
        catalog.sort()
        return catalog[-1]

def copy_files(args=None, source=None, destination=None, snapshot=None):
    """Copy all files between source and destination."""
    if not source:
        source = 'current_dir'
        if not os.path.exists('current_dir'):
            print('Directory current_dir does not exist; exiting')
            sys.exit()
    # Get last backup dir and create directory for next backups, if needed.
    if not destination:
        snapshot = get_highest_snapshot() + 1
        destination = os.path.join('.myvcs', str(snapshot))
    # Copy whole directory.
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    print('Copied files from\n    {}\nto\n    {}.'.
            format(source, destination))
    with open(os.path.join('.myvcs', 'HEAD'), 'w') as f:
        f.write(str(snapshot))

def print_current_head(args=None):
    with open(os.path.join('.myvcs', 'HEAD'), 'r') as f:
        head = f.read()
    print(head)

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

