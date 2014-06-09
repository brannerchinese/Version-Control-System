#! /usr/bin/env python
# myvcs.py
# David Prager Branner
# 20140605

import difflib as D
import os
import argparse

def main():
    # QQQ This should happen only on initialization.
    if '.myvcs' not in os.listdir():
        os.mkdir('.myvcs')
        ordinal = 0
    else:
        catalog = sorted([int(i) for i in os.listdir('.myvcs')])
        print(catalog)
        ordinal = catalog[-1] + 1
    # Form diffs of files.
    content = ''
    # Store diffs; 
    with open('.myvcs/' + str(ordinal), 'w') as f:
        f.write(content)

if __name__ == '__main__':
    main()
