import os

import numpy as np
import pandas as pd
from scipy.signal import periodogram


def calc_spectral_ratios(signal, fs, f_low=5, f_med=25, f_high=70):
    """
    Return the power ratio contained in 3 bands.
    0 - LF, LF - MF, and MF - HF.

    """
    # Calculate power spectrum using periodogram
    f, pxx = periodogram(signal, fs)

    # Relative areas
    if np.where(f > f_low)[0].size:
        a1 = np.sum(pxx[np.where(f > -1)[0][0]:np.where(f > f_low)[0][0]])
        if np.where(f > f_med)[0].size:
            a2 = np.sum(pxx[np.where(f > f_low)[0][0]:np.where(f > f_med)[0][0]])
            if np.where(f > f_high)[0].size:
                a3 = np.sum(pxx[np.where(f > f_med)[0][0]:np.where(f > f_high)[0][0]])
            else:
                a3 = 1 - a1 - a2
        else:
            a2 = 1 - a1
            a3 = 0
    else:
        a1 = 1
        a2 = 0
        a3 = 0

    a_total = a1 + a2 + a3

    # If there is no spectral power. ie. signal is flatline.
    if a_total == 0:
        return 1, 0 ,0

    return a1 / a_total, a2 / a_total, a3 / a_total
