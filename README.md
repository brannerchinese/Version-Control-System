## Version Control System

Simple version control system.

This project was done as part of the [Iron Forger](https://hackpad.com/Week-3-Make-a-Local-Version-Control-System-NZ1n98nFktQ), which some alums of [Hacker School](http://hackerschool.com) organized in the summer of 2014. Please see the description at that link for the goals of the assignment and other completed versions of the project.

### How to install and run.

 1. Runs only under Python 3.3 and higher.
 1. In directory `vcs`, run as `./myvcs.py` at the command line. Program backs up the contents of directory `current_dir` to a "snapshot" in a numbered subdirectory of `.myvcs` and saves that subdirectory's number to a file `.myvcs/HEAD`. If `current_dir` does not exist, the program exits.
 1. Successive runs of `./myvcs.py` create successive subdirectories and make successive snapshots. No attempt is made to see if the contents have changed, and all contents are saved entire. Using `./myvcs.py backup` will have the same effect. Current system date and time (in Unix time) are saved, too, to a file `DATE` in the new subdirectory, and the most recent value of `.myvcs/HEAD` is saved to a file `PARENT` in the new subdirectory.
 1. A message (like a Git commit-message) can be saved along with a snapshot by using `./myvcs.py backup -m "your message here"`. This message is saved to a file `MESSAGE` in the new subdirectory.
 1. To print the subdirectory-number of the current snapshot, without changing it, use `./myvcs.py current`.
 1. To change the current snapshot to snapshot 3, use `./myvcs.py checkout 3`, etc. etc.
 1. To print the history of all snapshots from the current one backward until there are no more parent-snapshots found, use `./myvcs.py log`.

### Future work.

 1. It would be more efficient if the system archived only diffs rather than actual files. A diff-patching tool is needed to regenerate files. But the code to copy files (`copy_files`) would have to be more complicated, and in particular something more sophisticated than `shutil.copytree` would be needed for traversing the directory.
 1. It seems that section 2.1 of the assignment ("Branches") is not meaningful without the capacity for merging, otherwise a given snapshot can only have one ancestor.
 1. It would be best if the whole present directory were backed up, rather than only a subdirectory `current_dir`. 
 1. The basic functionality described above has been tested manually. There is no test suite.

[end]
