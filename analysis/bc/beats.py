import os

import matplotlib.pyplot as plt
import numpy as np


def get_beats(sig, beat_inds, prop_left=0.3, rr_limits=(108, 720),
              view=False):
    """
    Given a signal and beat locations, extract the beats.
    Beats are taken as prop_left of the signal fraction to the previous
    beat, and 1-prop_left of the signal fraction to the next beat.

    Exceptions are for the first beat, last beat, and when the
    next beat is too close or far.

    Paramters
    ---------
    sig : numpy array
        The 1d signal array
    beat_inds : numpy array
        The locations of the beat indices
    prop_left : float, optional
        The fraction/proportion of the beat that lies to the left of the
        beat index. The remaining 1-prop_left lies to the right.
    rr_limits : tuple, optional
        Low and high limits of acceptable rr values. Default limits 108
        and 720 samples correspond to 200bpm and 30bpm at fs=360.
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
    sig_len = len(sig)
    n_beats = len(beat_inds)

    # List of numpy arrays of beat segments
    beats = []
    # qrs complex detection index relative to the start of each beat
    centers = []
    # rr intervals, used to extract beats
    rr = np.diff(beat_inds)
    mean_rr = np.average(rr[(rr < rr_limits[1]) & (rr > rr_limits[0])])

    for i in range(n_beats):
        if i == 0:
            len_left = rr[0]

        # Previous and next rr intervals for this qrs
        rr_prev = rr[max(0, i - 1)]
        rr_next = rr[min(i, n_beats-2)]

        # Constrain the rr intervals
        if  not rr_limits[0] < rr_prev < rr_limits[1]:
            rr_prev = mean_rr
        if  not rr_limits[0] < rr_next < rr_limits[1]:
            rr_next = mean_rr

        len_left = int(rr_prev * prop_left)
        len_right = int(rr_next * prop_right)

        # Skip beats too close to boundaries
        if beat_inds[i] - len_left < 0 or beat_inds[i] + len_right > sig_len-1:
            continue

        beats.append(sig[beat_inds[i] - len_left:beat_inds[i] + len_right])
        centers.append(len_left)

        if view:
            # Viewing results
            print('len_left:', len_left, 'len_right:', len_right)
            plt.plot(beats[-1])
            plt.plot(centers[-1], beats[-1][centers[-1]], 'r*')
            plt.show()

    return beats, centers


def get_beat_bank(start_sec=280, stop_sec=300):
    """
    Make a beat bank of ecgs by extracting all beats from
    the same time section of channels 0 and 1 of all true
    alarm training records.
    """
    fs = 250
    beat_bank = {}
    # No cheating! We should only have access to training data
    records_train, records_test = train_test_split(record_names)

    for record_name in records_train:
        # Skip false alarm records
        if not alarms.loc[record_name, 'result']:
            continue
        # Read record
        signal, fields = wfdb.rdsamp(os.path.join(data_dir, record_name),
                                     sampfrom=start_sec*fs, sampto=stop_sec*fs,
                                     channels=[0, 1])
        # Determine which signals are valid
        valid = is_valid(signal)

        # Clean the signals, removing nans
        signal = fill_missing(sig=signal)
        # Filter the signal
        signal = bandpass(signal, fs=fs, f_low=0.5, f_high=40, order=2)

        # Get beats from each channel
        for ch in range(2):
            sig_ch = signal[:, ch]
            sig_name = fields['sig_name'][ch]

            # Skip the signals with too few instances
            if sig_name.startswith('aV'):
                continue

            # Skip flatline signals
            if not valid[ch]:
                continue

            # Get beat locations
            qrs_inds = processing.xqrs_detect(sig_ch, fs=fs,
                                              verbose=False)
            # Skip if too few beats
            if len(qrs_inds) < 2:
                continue
            # Normalize the signal
            sig_ch = normalize(sig_ch)
            # Get the beats
            beats, _ = get_beats(sig_ch, qrs_inds)
            if sig_name not in beat_bank.keys():
                beat_bank[sig_name] = []
            beat_bank[sig_name] = beat_bank[sig_name] + beats
    print('Finished obtaining beat bank')

    # Remove signals without beats from the dictionary
    for sig_name in beat_bank:
        if len(beat_bank[sig_name]) == 0:
            print('Obtained no beats for signal %s. Removing.' % sig_name)
            del(beat_bank[sig_name])
    return beat_bank
