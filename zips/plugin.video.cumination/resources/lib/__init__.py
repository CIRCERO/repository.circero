import inspect
import os, sys
import os.path
files = os.listdir(os.path.dirname(__file__))
__all__ = [filename[:-3] for filename in files if not filename.startswith('__') and filename.endswith('.py')]
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

