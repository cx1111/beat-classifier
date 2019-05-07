import matplotlib.pyplot as plt
import numpy as np

from .beats import BEAT_TYPES, SIG_NAMES


def plot_beat(sig, center, style='C0', figsize=(6.4, 4.8),
              sig_names=SIG_NAMES, title='', seconds=True):
    """
    Plot a beat and center. Single or multi-channel.

    """
    fs = 360
    plt.figure(figsize=figsize)

    if sig.ndim > 1:
        if seconds:
            t = np.arange(0, sig.shape[0]/fs, 1/fs)
        else:
            t = np.arange(0, sig.shape[0])

        for ch in range(sig.ndim):
            plt.subplot(2, 1, ch+1)
            if ch == 0:
                plt.title(title)
            plt.plot(t, sig[:, ch], style)
            plt.plot(t[center], sig[center, ch], 'k*')
            plt.xlabel('time/{}'.format('second' if seconds else 'sample'))
            plt.ylabel('{}/mV'.format(sig_names[ch]))
    else:
        if seconds:
            t = np.arange(0, sig.shape[0]/fs, 1/fs)
        else:
            t = np.arange(0, sig.shape[0])
        plt.plot(t, sig, style)
        plt.plot(t[center], sig[center], 'k*')
        plt.xlabel('time/{}'.format('second' if seconds else 'sample'))
        sig_name = sig_names if isinstance(sig_names, str) else sig_names[0]
        plt.ylabel('{}/mV'.format(sig_name))

    plt.show()


def plot_four_beats(beats, centers, figsize=(16, 9), seconds=True):
    """
    Plot and compare the four different beat types.

    Parameters
    ----------
    beats : list
        list of four Mx2 numpy arrays of beats
    centers : list
        list of four integers of the beat centers

    """
    plt.figure(figsize=figsize)

    fs = 360
    styles = ['C0', 'C1', 'C2', 'C3']

    for beatnum in range(4):
        sig_len = beats[beatnum].shape[0]
        t = np.arange(0, sig_len/fs, 1/fs) if seconds else np.arange(0, sig_len)
        for ch in range(2):
            plt.subplot(4, 2, beatnum*2 + ch + 1)
            if beatnum == 0:
                plt.title('Channel {}'.format(SIG_NAMES[ch]))
            plt.plot(t, beats[beatnum][:, ch], styles[beatnum])
            plt.plot(t[centers[beatnum]], beats[beatnum][centers[beatnum], ch], 'k*')
            plt.legend([BEAT_TYPES[beatnum]])
            plt.ylabel('{}/mV'.format(SIG_NAMES[ch]))
            if beatnum == 3:
                plt.xlabel('time/{}'.format('second' if seconds else 'sample'))
    plt.show()
