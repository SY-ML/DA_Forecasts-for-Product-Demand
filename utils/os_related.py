import os

def make_direction(path):
    try:
        os.mkdir(path)
    except:
        pass