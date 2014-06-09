#! /usr/bin/env python
# diff_patch.py
# David Prager Branner
# 20140608

"""Provide diff and patch functionality based on Python difflib."""

import difflib as D
import os

def diff(directory, from_file, to_file, diff_file):
    """Generate a narrow diff from two input files."""
    # Get contents of files.
    with open(os.path.join(directory, from_file), 'r') as f:
        from_contents = f.read()
    from_contents = [i + '\n' for i in from_contents.split('\n')]
    with open(os.path.join(directory, to_file), 'r') as f:
        to_contents = f.read()
    to_contents = [i + '\n' for i in to_contents.split('\n')]
    # Process with unified_diff.
    difftext = D.unified_diff(
            from_contents, to_contents, from_file, to_file, n=0)
    # Save difftext.
    with open(os.path.join(directory, diff_file), 'w') as f:
        f.write(''.join(list(difftext)))

def patch(directory, diff_file, known_filename):
    """Reconstruct a missing file from a diff and a second file."""
    # Retrieve diff_file and known_file.
    with open(os.path.join(directory, diff_file), 'r') as f:
        difftext = f.read()
    difftext = (i for i in difftext.split('\n'))
    with open(os.path.join(directory, known_filename), 'r') as f:
        known_file = f.read()
    known_file = (i for i in known_file.split('\n'))
    # Read diff header and decide whether known_file is from_file or to_file.
    minus = next(difftext).split()[1]
    plus = next(difftext).split()[1]
    print('minus: {}\nplus:  {}'.format(minus, plus))
    if known_filename == minus:
        recovered_file = advance(plus, known_file, difftext)
    elif known_filename == plus:
        recovered_file = regress(minus, known_file, difftext)
    else:
        raise Exception('known_file {} is not found in the diff file.'.
            format(known_filename))
    return recovered_file

def advance(recovered_filename, known_file, difftext):
    # Step through difftext and process each line (numbered from 1).
    current_line = 1
    last_current = 1
    recovered_file = []
    while True:
        try:
            nextline = next(difftext)
        except StopIteration:
            break
        # If next line is start of hunk, decide what needs to be done.
        if nextline[0:2] == '@@':
            # Get the values needed
            nextline = nextline.split()
            print('Found next hunk: {}'.format(nextline))
            to_skip = nextline[1][1:].split(',')
            to_insert = nextline[2][1:].split(',')
            if len(to_skip) == 1:
                skip_how_many = 1
            else:
                skip_how_many = int(to_skip[1])
            if len(to_insert) == 1:
                insert_how_many = 1
            else:
                insert_how_many = int(to_insert[1])
            print('to skip: {} lines; to insert: {} lines'.
                    format(skip_how_many, insert_how_many))
            #
            # Copy any foregoing lines.
            current_line = int(to_skip[0])
            print('current_line: {}; last_current: {}'.
                    format(current_line, last_current))
            to_copy = current_line - last_current
            if skip_how_many:
                to_copy -= 1
            print('lines to copy: {}'.format(to_copy))
            last_current = current_line
            print('Foregoing lines to print: {}'.format(to_copy))
            for line in range(to_copy):
                recovered_file.append(next(known_file))
                print('copied line:\n    {}'.format(recovered_file[-1]))
            #
            # Skip any lines to be skipped
            for line in range(skip_how_many):
                try:
                    _ = next(known_file)
                except StopIteration:
                    break
                print('skipped line:\n    {}'.format(_))
            #
            # Add any new lines to be added
            while insert_how_many: 
                try:
                    nextline = next(difftext)
                except StopIteration:
                    break
                if nextline[0] == '+':
                    recovered_file.append(nextline[1:])
                    insert_how_many -= 1
                    print('added line:\n    {}'.format(recovered_file[-1]))
                elif nextline[0] == '-':
                    print('ignoring From line:\n    {}'.format(nextline))
        else:
            print('no action on line:\n    {}'.format(nextline))
        print('recovered_file now:', recovered_file)
        print('done with this loop\n')
    return recovered_file

def regress(recovered_filename, known_file, difftext):
    # Step through difftext and process each line.
    instructions = 0
    while True:
        try:
            nextline = next(difftext)
        except StopIteration:
            break
        if nextline[0:2] == '@@':
            # New set of instructions.
            nextline = nextline.split()
            print('lines of instruction up to now: {}'.format(instructions))
            print('nextline: {}'.format(nextline))
            instructions = 0
        else:
            # Instructions.
            instructions += 1
            pass
    return recovered_file
