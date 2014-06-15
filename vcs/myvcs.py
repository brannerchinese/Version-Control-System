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
            'backup': new_backup,
            }
    if not args:
        new_backup()
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
        snapshot = snapshot[0]
    print('snapshot: {}'.format(snapshot))

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
        print('catalog: {}'.format(catalog))
        return catalog[-1]

def new_backup(args=None):
    # Get last backup dir and create directory for next backups, if needed.
    next_backup_dir = get_working_mvc_dir()
    print(next_backup_dir)
    #
    # Traverse subdirectories.
    current_dir = os.getcwd()
    print('current_dir:', current_dir)
    walker = os.walk(current_dir)
    while True:
        try:
            present, next_dirs, files = next(walker)
        except StopIteration:
            break
        present = present.replace(current_dir, '').lstrip('/')
        print('present: ', present)
        if present in myvcs_ignore:
            print('    continuing because {} in myvcs_ignore'.format(present))
            continue
        next_dirs[:] = [i for i in next_dirs if i not in myvcs_ignore]
        files[:] = [i for i in files if i not in myvcs_ignore]
        print('next_dirs: {}'.format(next_dirs))
        if files:
            if present not in myvcs_ignore:
                copy_to_dir = os.path.join(next_backup_dir, present)
                if not os.path.exists(copy_to_dir):
                    os.mkdir(copy_to_dir)
                print('copy_to_dir:', copy_to_dir)
                for f in files:
                    print('    now trying {}'.format(f))
                    shutil.copy2(os.path.join(present, f), copy_to_dir)
    print('Done.')

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
    head_dir = os.path.join('.myvcs', str(head))
    try:
        os.mkdir(head_dir)
    except Exception as e:
        print(e)
        sys.exit(1)
    with open(os.path.join('.myvcs', 'HEAD'), 'w') as f:
        f.write(str(head))
    return head_dir

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

