# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy.stats

def ppg_simulate(duration=10, length=None, sampling_rate=1000, noise=0.01, heartrate=60):
    """Simulate a PPG (photoplethysmography) signal

    **This functions is not ready and help is required to implement it.**
    Generate an artificial (synthetic) PPG signal of a given duration and sampling rate.

    Parameters
    ----------
    duration : int
        Desired recording length in seconds.
    sampling_rate, length : int
        The desired sampling rate (in Hz, i.e., samples/second) or the desired
        length of the signal (in samples).
    noise : float
       Noise level (gaussian noise).
    heartrate : int
        Desired simulated heart rate (in beats per minute).

    Returns
    ----------
   array
        Array containing the PPG signal.

    Examples
    ----------
    >>> import neurokit2 as nk
    >>>
    >>> ppg = nk.ppg_simulate(duration=10)
    >>> nk.signal_plot(ppg)

    See Also
    --------
    signal_resample, ecg_simulate, emg_simulate


    References
    ----------
    - `Banerjee et al. (2015). Noise cleaning and Gaussian modeling of smart phone photoplethysmogram to improve blood pressure estimation. In 2015 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 967-971). IEEE. <http://150.162.46.34:8080/icassp2015/pdfs/0000967.pdf>`_.

    """
    index = np.linspace(-9, 9, num=100)
    normal1 = scipy.stats.norm.pdf(index, loc=-2, scale=2)/1.5
    normal2 = scipy.stats.norm.pdf(index, loc=2, scale=1.5)
    ppg = normal1+normal2
    # pd.Series(ppg).plot()
    return ppg
