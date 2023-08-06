import numpy as np
import scipy.signal as sigpy
import matplotlib.pyplot as plt

def rect(T):
    """create a centered rectangular pulse of width $T"""
    return lambda t: (-T/2 <= t) & (t < T/2)

def pulse_train(t, at, shape):
    """create a train of pulses over $t at times $at and shape $shape"""
    return np.sum(shape(t - at[:,np.newaxis]), axis=0)

def phaseshifting ( alpha, f, t , phase = 0):
    """ Creates a phase controlled waveform. alpha describes the switching point """
    omega = np.pi * 2 * f
    w = alpha / omega
    d = np.arange ( .5/f, t[-1], .5/f )
    d = d - .5*w - phase/omega;
    y = np.sin( omega * t + phase);

    y2 = pulse_train(
        t=t,                           # time domain
        at=d,                          # times of pulses
        shape=rect(w)                  # shape of pulse
    )
    return y*y2

def fhwm ( x, y, trsh = .5):
    """ calculates the fullwidth height maximum """
    max_val,max_idx = np.amax(y), np.argmax(y)
    min_left_idx = np.argmin ( np.abs ( y[0:max_idx - 1] - max_val * trsh ))
    min_right_idx = np.argmin ( np.abs ( y[max_idx:-1] - max_val * trsh ))
    min_right_idx += (max_idx - 1)
    tp = x[min_right_idx] - x[min_left_idx]
    return min_left_idx, min_right_idx, tp

def PitchDetection(Samples,
          fs,
          window=np.hanning,
          partials=5 ):

    N = Samples.size
    N2 = int(2**np.log2(N))
    wdw = window(N)

    frequencies = np.fft.fftfreq(N2, d=1./fs )
    spectrum = 2*np.abs(np.fft.fft( wdw*Samples, N2 )) / N2

    # Downsample spectrum.
    spectra = []
    for n in range(1, partials + 1):
        s = sigpy.resample(spectrum, N2 // n)
        spectra.append(s)

    a = np.zeros(( partials , N2), dtype=spectrum.dtype)

    for i, s in enumerate(spectra):
        ll = len(s)
        a[i, 0:ll] = s

    hps = np.product(np.abs(a), axis=0) / partials

    fIdx = np.argmax ( hps[0:N2//2] )
    return frequencies[fIdx]

def undelay_td_series ( y1, y2, fs, same = False  ):
    """ calculates the delay between two signals using cross correlation """
    xcorr  = np.correlate(y1, y2, "same")
    if same == True:
        delay_arr = np.linspace(0, y1.size/fs, y1.size)
    else:
        delay_arr = np.linspace(-0.5*y1.size/fs, 0.5*y1.size/fs, y1.size)
    return delay_arr[np.argmax(xcorr)]
