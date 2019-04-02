import os

def getLabelsFromDir(directory):
    """
    return list of names of subdirectories
    e.g. ["subdir1", "subdir2", "subdir3"]
    """
    out = [sub for sub in os.listdir(directory) if os.path.isdir(os.path.join(directory,sub))]
    return out