import numpy as np
from plyfile import PlyData, PlyElement

def read_calib_file(filepath):
    # Read in a calibration file and parse into a dictionary.
    # https://github.com/utiasSTARS/pykitti/blob/master/pykitti/utils.py
    data = {}
    with open(filepath, 'r') as f:
        for line in f.readlines():
            key, value = line.split(':', 1)
            try:
                data[key] = np.array([float(x) for x in value.split()])
            except ValueError:
                pass
    return data

def read_ply(fn):
    print('Reading {}'.format(fn))
    plydata = PlyData.read(fn)
    x = plydata['vertex']['x']
    y = plydata['vertex']['y']
    z = plydata['vertex']['z']
    pts = np.array([x,y,z]).T
    return np.array([x,y,z]).T # (nv,3)
    return pts

