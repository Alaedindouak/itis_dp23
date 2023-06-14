import os

def fpath(dirname, fname=''):
   return os.path.join(
      os.path.dirname(os.path.abspath(__file__)),
      dirname,
      fname
   )