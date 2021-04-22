#%%
import numpy as np
import h5py
import sys


def save(varlist, filename=None, mode='w'):
    # formatting the inputs
    if isinstance(varlist, str):
        varlist = [varlist] # make it a list so that the following code work
    if filename == None:
        filename = varlist[0] + '.h5'
        
    # note that this next line is not a very good practice.
    # just being lazy...
    caller = sys._getframe(1)

    # save variables into a file
    with h5py.File(filename, mode) as f:
        for vname in varlist:
            f.create_dataset(vname, data=caller.f_locals[vname])


def load(filename):

    output = {}
    with h5py.File(filename, 'r') as f:
        for key in f.keys():
            output[key] = np.array(f[key])
    
    return output
            


