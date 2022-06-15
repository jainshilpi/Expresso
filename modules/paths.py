import os
import modules
pjoin = os.path.join

def IHEP_path(path):
    return pjoin(modules.__path__[0], path)
