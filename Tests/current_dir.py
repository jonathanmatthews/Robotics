import inspect
import sys
import os

current_dir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))
parentdir = os.path.dirname(current_dir)
sys.path.insert(0, parentdir)
