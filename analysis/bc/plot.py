import matplotlib.pyplot as plt


def plot_beat(sig, center, style='C0', figsize=(6.4, 4.8),
              sig_names=['MLII', 'V1'], title=''):
    """
    Plot a beat and center.

    """
    plt.figure(figsize=figsize)

    if sig.ndim > 1:
        for ch in range(sig.ndim):
            plt.subplot(2, 1, ch+1)
            if ch == 0:
                plt.title(title)
            plt.plot(sig[:, ch], style)
            plt.plot(center, sig[center, ch], 'k*')
            plt.xlabel('time/sample')
            plt.ylabel('{}/mV'.format(sig_names[ch]))
    else:
        plt.plot(sig)
        plt.plot(center, sig[center], style)
        plt.plot(center, sig[center], 'k*')
        plt.xlabel('time/sample')
        sig_name = sig_names if isinstance(sig_names, str) else sig_names[0]
        plt.ylabel('{}/mV'.format(sig_name))

    plt.show()


def plot_four_beats(beats, centers, figsize=(16, 9)):
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

    titles = ['Normal', 'LBBB', 'RBBB', 'Ventricular']
    styles = ['C0', 'C1', 'C2', 'C3']
    sig_names = ['MLII', 'V1']

    for beatnum in range(4):
        for ch in range(2):
            plt.subplot(4, 2, beatnum*2 + ch + 1)
            plt.plot(beats[beatnum][:, ch], styles[beatnum])
            plt.plot(centers[beatnum], beats[beatnum][centers[beatnum], ch], 'k*')
            plt.legend([titles[beatnum]])
            plt.xlabel('time/sample')
            plt.ylabel('{}/mV'.format(sig_names[ch]))

    plt.show()

