# these lines attempt to load any turtle code present, looking for a file called
# turtlecode.py
#
# delete these lines to use CircuitPy normally
try:
    import turtlecode
except ImportError:
    import run_calibration
