import os

import numpy as np


def find_baseline(sig, inspect_prop=0.2):
    """
    Find the baseline of an ecg signal
    """
    # Find the flattest parts of the left segment of the signal
    dy = np.diff(sig[:int(len(sig)*inspect_prop)])


    # Get the mean of the flattest regions at the start and end



    return baseline


def segment_beat(sig, center):
    """
    Segment a single heartbeat, given the signal and its r center

    """

    # Gradients
    dy = np.diff(sig)



    return p0, p1, p2,




