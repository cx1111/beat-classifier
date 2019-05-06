import numpy as np
from scipy.signal import butter, filtfilt


def filter_band(sig, btype, fs=360, f_low=0.5, f_high=40, order=4):
    """
    Bandpass or bandstop filter the signal
    """
    if sig.ndim ==2:
        sig_filt = np.zeros(sig.shape)
        for ch in range(sig.shape[1]):
            sig_filt[:, ch] = bandpass(sig[:, ch], fs, f_low, f_high, order)
        return sig_filt

    if btype not in ['band', 'stop']:
        raise ValueError('btype must be band or stop.')

    f_nyq = 0.5 * fs
    wlow = f_low / f_nyq
    whigh = f_high / f_nyq
    b, a = butter(order, [wlow, whigh], btype=btype)
    sig_filt = filtfilt(b, a, sig, axis=0)

    return sig_filt


def normalize(sig):
    """
    Normalize a signal to zero mean unit std
    """
    if np.ptp(sig) == 0:
        return sig

    return (sig - np.average(sig)) / np.std(sig)
