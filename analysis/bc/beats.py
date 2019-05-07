import os

import matplotlib.pyplot as plt
import numpy as np
import wfdb

from .io import ann_to_df
from .preprocess import filter_band


BEAT_TYPES = ['Normal', 'LBBB', 'RBBB', 'Ventricular']

SIG_NAMES = ['MLII', 'V1']


def get_beats(sig, qrs_inds, beat_types, wanted_type, prop_left=0.3,
              rr_limits=(108, 540), fixed_width=None, single_chan=False,
              view=False):
    """
    Given a signal and beat locations, extract the beats of a certain
    type.

    Beats are taken as prop_left of the signal fraction to the previous
    beat, and 1-prop_left of the signal fraction to the next beat.

    Exceptions are for the first beat, last beat, and when the
    next beat is too close or far.

    Paramters
    ---------
    sig : numpy array
        The single or multi-channel signal.
    qrs_inds : numpy array
        The locations of the beat indices.
    beat_types : list
        The labeled beat types.
    wanted_type : str
        The type of beat to extract. All others will be skipped, though
        their qrs locations will be used to calculate beat boundaries.
    prop_left : float, optional
        The fraction/proportion of the beat that lies to the left of the
        beat index. The remaining 1-prop_left lies to the right.
    rr_limits : tuple, optional
        Low and high limits of acceptable rr values. Default limits 108
        and 540 samples correspond to 200bpm and 40bpm at fs=360.
    fixed_width : int, optional
        If set, this returns beats of width specified by this parameter,
        continuing to use `prop_left` but ignoring `rr_limits`.
    single_chan : bool, optional
        If sig has more than 1 channel, specifies whether to keep only
        the first channel. Option ignored if sig has one channel.
    view : bool, optional
        Whether to display the individual beats collected

    Returns
    -------
    beats : list
        List of numpy arrays representing beats.
    centers : list
        List of relative locations of the beat centers for each beat
    """
    prop_right = 1 - prop_left
    sig_len = sig.shape[0]
    n_beats = len(qrs_inds)

    # List of numpy arrays of beat segments
    beats = []
    # qrs complex detection index relative to the start of each beat
    centers = []
    # rr intervals, used to extract beats
    rr = np.diff(qrs_inds)
    mean_rr = np.average(rr[(rr < rr_limits[1]) & (rr > rr_limits[0])])

    for i in range(n_beats):
        # Only keep wanted beat types
        if beat_types[i] == wanted_type:

            if fixed_width is None:
                # Previous and next rr intervals for this qrs
                rr_prev = rr[max(0, i - 1)]
                rr_next = rr[min(i, n_beats-2)]

                # Constrain the rr intervals
                if not (rr_limits[0] < rr_prev < rr_limits[1]):
                    rr_prev = mean_rr
                if not (rr_limits[0] < rr_next < rr_limits[1]):
                    rr_next = mean_rr
                len_left = int(rr_prev * prop_left)
                len_right = int(rr_next * prop_right)
            else:
                len_left = int(fixed_width * prop_left)
                len_right = fixed_width - len_left

            # Skip beats too close to boundaries
            if qrs_inds[i] - len_left < 0 or qrs_inds[i] + len_right > sig_len-1:
                continue

            if sig.ndim == 1:
                beats.append(sig[qrs_inds[i] - len_left:qrs_inds[i] + len_right])
            else:
                if single_chan:
                    beats.append(sig[qrs_inds[i] - len_left:qrs_inds[i] + len_right, 0])
                else:
                    beats.append(sig[qrs_inds[i] - len_left:qrs_inds[i] + len_right, :])
            centers.append(len_left)

            if view:
                # Viewing results
                plt.plot(beats[-1])
                plt.plot(centers[-1], beats[-1][centers[-1]], 'r*')
                plt.show()

    return beats, centers


def get_beat_bank(data_dir, beat_table, wanted_type, single_chan=False,
                  filter_beats=False, fixed_width=None, min_len=1):
    """
    Make a beat bank of ecgs by extracting all beats from the records
    from MITDB containing at least `min_len` seconds of that type of
    beat, according to the table of beat information `beats_df`.

    40/48 of the records have channels MLII and V1.
    Skip the records with different channels.

    """
    # records with alternative channel sets
    ALT_SIG_RECORDS = ['100', '102', '103', '104', '114', '117', '123', '124']

    records = beat_table.loc[beat_table[wanted_type]>=min_len].index.values

    all_beats, all_centers = [], []
    for rec_name in records:
        # Skip the records with different channels
        if rec_name not in ALT_SIG_RECORDS:
            # Load the signals and beat annotations
            sig, fields = wfdb.rdsamp(os.path.join(data_dir, rec_name))

            if filter_beats:
                sig = filter_band(sig, btype='band', f_low=0.5, f_high=40)
                sig = filter_band(sig, btype='stop', f_low=55, f_high=65)

            ann = wfdb.rdann(os.path.join(data_dir, rec_name), extension='atr')
            # Get the peak samples and symbols in a dataframe. Remove
            # the non-beat annotations
            qrs_df = ann_to_df(ann, rm_sym=['+', '~'])
            # Get the beats and centers of the record
            beats, centers = get_beats(sig=sig, qrs_inds=qrs_df['sample'].values,
                beat_types=qrs_df['symbol'].values, wanted_type=wanted_type,
                single_chan=single_chan, fixed_width=fixed_width)

            all_beats += beats
            all_centers += centers

    return all_beats, all_centers
