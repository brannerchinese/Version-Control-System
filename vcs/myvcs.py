#! /usr/bin/env python
# myvcs.py
# David Prager Branner
# 20140614

import sys
if sys.version_info.major < 3 and sys.version_info.minor < 3:
    print('At least Python 3.3 is required to run this program.')
    sys.exit(0)
import difflib as D
import os
import argparse
import collections

myvcs_ignore = {'.myvcs', '.myvcs.py.swp', '__pycache__', 'myvcs.py'}

def main():
    # Get directory for current backups.
    backup_dir = get_working_mvc_dir()
    print(backup_dir)
    os.mkdir(backup_dir)
    # Get list of all files in present directory.
    current_dir = os.getcwd()
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

def get_working_mvc_dir():
    # QQQ This should happen only on initialization.
    if '.myvcs' not in os.listdir():
        os.mkdir('.myvcs')
        ordinal = 0
    else:
        # Use loop rather than comprehension so as to allow try-block.
        catalog = []
        for i in os.listdir('.myvcs'):
            try:
                catalog.append(int(i))
            except ValueError:
                continue
        catalog.sort()
        print('catalog: {}'.format(catalog))
        ordinal = catalog[-1] + 1
    # Copy files into .myvcs/ordinal/ recursively.
    working_dir = '.myvcs/' + str(ordinal)
    return working_dir

if __name__ == '__main__':
    main()
