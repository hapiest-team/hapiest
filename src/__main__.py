"""
This is the main module. It basically checks that there is a hapi api key, asks for one if there
is not one, and launches the main GUI. That's about it.
"""
import sys, os

if getattr(sys, 'frozen', False):
    os.environ['JOBLIB_MULTIPROCESSING'] = '0'

from multiprocessing import freeze_support, set_start_method
multiprocessing.set_start_method('forkserver', force=True)
freeze_support()

from startup import fix_cwd, check_version

check_version()
fix_cwd()

from app import run

if __name__ == '__main__':
    print(sys.argv)
    import traceback

    try:
        sys.exit(run())
    except TypeError as err:
        print("Encountered type error:\n" + str(err))
        traceback.print_exc()
    except Exception as err:
        print("Encountered an error: \n" + str(err))
        traceback.print_exc()
