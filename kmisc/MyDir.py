import os
def MyDir():
    if '__file__' in globals() : return os.path.dirname(os.path.realpath(__file__))
