from contextlib import contextmanager
import os


@contextmanager
def change_directory(path):
    '''
    Changes directory, moving back once the context manager is closed

    This returns the previous path (if needed) to the with statement
    '''
    previous_path = os.getcwd()

    try:
        # Go to the requested path
        os.chdir(path)
        yield previous_path
    finally:
        # Always return to where we were
        os.chdir(previous_path)
