import numpy as np
from scipy.stats import poisson
import h5py
import sys


# IO related
def save(varlist, filename=None, mode="w"):
    # formatting the inputs
    if isinstance(varlist, str):
        varlist = [varlist]  # make it a list so that the following code work
    if filename == None:
        filename = varlist[0] + ".h5"

    # note that this next line is not a very good practice.
    # just being lazy...
    caller = sys._getframe(1)

    # save variables into a file
    with h5py.File(filename, mode) as f:
        for vname in varlist:
            f.create_dataset(vname, data=caller.f_locals[vname])


def load(filename):

    output = {}
    with h5py.File(filename, "r") as f:
        for key in f.keys():
            output[key] = np.array(f[key])

    return output


# spiking data analysis
def quasi_poisson_sig_test(response_counts, window_size, spont_fr, spont_disper):

    # is the windowsize ms or s?
    ntrials = response_counts.size
    expected_counts = spont_fr * window_size * ntrials
    actual_counts = response_counts.sum()

    k = actual_counts / spont_disper
    mu = expected_counts / spont_disper
    pval = 1 - poisson.cdf(k, mu)
    return pval


def quasi_poisson_sig_test_fr(response_fr, duration, spont_fr, spont_disper):
    expected_counts = spont_fr * duration
    actual_counts = response_fr * duration

    k = actual_counts / spont_disper
    mu = expected_counts / spont_disper
    pval = 1 - poisson.cdf(k, mu)
    return pval


# array manipulation
def center_of_mass(nparray, axis):
    # contains 0, 1, 2, ...
    indexlist = np.array(range(nparray.shape[axis]))
    indexlist = np.swapaxes(indexlist, 0, axis)
    return (nparray * indexlist).sum(axis=axis) / nparray.sum(axis=axis)
