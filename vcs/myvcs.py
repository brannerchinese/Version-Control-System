#! /usr/bin/env python
# myvcs.py
# David Prager Branner
# 20140617

import sys
if sys.version_info.major < 3 and sys.version_info.minor < 3:
    print('At least Python 3.3 is required to run this program.')
    sys.exit(0)
import difflib as D
import os
import argparse
import shutil
import time
import datetime

def main(args=None):
    actions = {
            'checkout': checkout,
            'latest': checkout,
            'backup': copy_files,
            'current': print_current_head,
            'log': print_log,
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

def print_log(args=None):
    """List parent, message, and date (if any), until no more parents found."""
    with open(os.path.join('.myvcs', 'HEAD'), 'r') as f:
        parent = f.read()
        print('Current head: {}'.format(parent))
    while parent:
        log_line = ''
        next_parent = os.path.join('.myvcs', str(parent), 'PARENT')
        if os.path.exists(next_parent):
            with open(next_parent, 'r') as f:
                parent = f.read()
                log_line += 'Parent: {}'.format(parent)
        else:
            parent = None
            break
        next_message = os.path.join('.myvcs', str(parent), 'MESSAGE')
        if os.path.exists(next_message):
            with open(next_message, 'r') as f:
                message = f.read()
        else:
            message = '(none)'
        log_line += '; Message: {}'.format(message)
        next_date = os.path.join('.myvcs', str(parent), 'DATE')
        if os.path.exists(next_date):
            with open(next_date, 'r') as f:
                date = f.read()
                date = convert_from_unixtime(float(date))
        else:
            date = '(none)'
        log_line += '; Date: {}'.format(date)
        print(log_line)

def copy_files(args=None, source=None, destination=None, snapshot=None):
    """Copy all files between source and destination."""
    if args and args[0] == '-m':
        message = args[1].strip("'\"")
    else:
        message = None
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
    # Store any message in MESSAGE, parent (= current HEAD), and date (Unixtime)
    if message:
        with open(os.path.join(destination, 'MESSAGE'), 'w') as f:
            f.write(message)
    with open(os.path.join('.myvcs', 'HEAD'), 'r') as f:
        parent = f.read()
        print('current HEAD => parent:', parent)
    with open(os.path.join(destination, 'PARENT'), 'w') as f:
        f.write(parent)
    with open(os.path.join(destination, 'DATE'), 'w') as f:
        f.write(str(time.time()))
    # Update HEAD.
    with open(os.path.join('.myvcs', 'HEAD'), 'w') as f:
        f.write(str(snapshot))
        print('saved new HEAD:', snapshot)

def convert_from_unixtime(unixtime, whole=True):
    """Convert Unix time to human-readable string."""
    if not whole:
        # Date only, no time.
        date = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d')
    else:
        # Both date and time.
        date = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d-%H%M')
    return date

def print_current_head(args=None):
    """Print current head."""
    with open(os.path.join('.myvcs', 'HEAD'), 'r') as f:
        head = f.read()
    print(head)

if __name__ == '__main__':
    main(sys.argv[1:])

