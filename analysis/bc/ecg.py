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


def right_indicator(env, env_p, W):
    """
    Given the windowed envelop signal env(t), and its peak env_p,
    compute the indicator function:
    A(t) = integral[t-W, t] [env(T) − env(t)]dT
    for the right segment of the envelope peak
    """
    # First check that the window doesn't overlap past the signal start
    # from the envelope peak
    i00 = env_p + 1 - W
    if i00 < 0:
        raise Exception('Window too large')

    a = np.zeros(len(env))

    # We only calculate a for values right of the envelope peak
    for t in range(env_p+1, len(env)):
        i0 = t - W
        a[t] = np.sum(env[i0:t]) - (env[t] * W)
        # a[t] = np.sum((env(T) - env(t)) for T in range(max(0, t-W), t))

    return a


def left_indicator(env, env_p, W):
    """
    Given the windowed envelop signal env(t), and its peak env_p,
    compute the indicator function:
    A(t) = integral[t, t+W] [env(T) − env(t)]dT
    for the left segment of the envelope peak
    """
    # First check that the window doesn't overlap past the signal end
    # from the envelope peak. Otherwise pad the signal to the right
    i11 = env_p - 1 + W
    overlap_len = i11 - len(env)
    if overlap_len > 0:
        env = np.append(env, np.repeat(env[-1], overlap_len))

    a = np.zeros(len(env))

    # We only calculate a for values left of the envelope peak
    for t in range(env_p-1):
        i1 = t + W
        a[t] = np.sum(env[t:i1]) - (env[t] * W)

    return a


def segment_beat(sig, qrs_p, fs=360, qrs_win_0=0.3, qrs_win_1=0.15,
                 max_qrs_duration=0.2):
    """
    Segment qrs_0 qrs_1

    Parameters
    ----------
    sig : the ecg beat signal
    qrs_p : the qrs peak index
    fs : sampling frequency of the signal
    qrs_win_0 : the search window for qrs onset, left of the peak
    qrs_win_1 : the search window for qrs offset, right of the peak
    max_qrs_t : maximum possible qrs time in seconds

    """
    sig_len = len(sig)

    # Filter the signal
    sig_f = bandpass(sig=sig, fs=fs, f_low=0.5, f_high=40, order=4)
    #sig_f = sig
    # Compute the envelope signal
    sig_h = hilbert(sig)
    sig_e = (sig_f**2 + np.abs(sig_h)**2) ** 0.5

    # Window the envelope signal based on the max possible qrs width
    # window_len = max_qrs_duration * fs

    # Window the envelope signal
    i0 = max(0, qrs_p-int(qrs_win_0*fs))
    i1 = min(qrs_p+int(qrs_win_1*fs), sig_len)
    env = sig_e[i0:i1]

    # The peak index of the envelope
    env_p = np.where(env==np.max(env))[0][0]

    # Ultimately we want (t2 − tp) < W < (t2 - t1)
    # The initial W needs to satisfy condition 1 and be larger than qrs1 - qrs_p
    # so half the max qrs duration should be big enough
    W0 = int(max_qrs_duration * fs / 2)
    # a = right_indicator(env=env, env_p=qrs_p-i0, W=W0)
    a = right_indicator(env=env, env_p=env_p, W=W0)
    # Get the point where a is max
    a_max = np.where(a==np.max(a))[0][0]

    # The second W should satisfy both conditions.
    # Set it to be a_max - env_p
    W1 = a_max - env_p
    a = right_indicator(env=env, env_p=env_p, W=W1)
    # This time, we take the location where the indicator is max
    # to be the final answer (adjust to start of full signal)
    qrs_1 = np.where(a==np.max(a))[0][0] + i0

    # Now do the left. Bigger starting window.
    W0 = int(max_qrs_duration * fs * 1)
    a = left_indicator(env=env, env_p=env_p, W=W0)
    a_max = np.where(a==np.max(a))[0][0]
    W1 = env_p - a_max
    a = left_indicator(env=env, env_p=env_p, W=W1)
    qrs_0 = np.where(a==np.max(a))[0][0]

    # Compute the


    return sig_f, sig_h, sig_e, env, qrs_0, qrs_1



