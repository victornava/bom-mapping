# get the path of the file being executed
import os
# get the path of the file being executed
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
print path
print dir_path