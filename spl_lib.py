#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Translated from a MATLAB script (which also includes C-weighting, octave
and one-third-octave digital filters).

Author: Christophe Couvreur, Faculte Polytechnique de Mons (Belgium)
        couvreur@thor.fpms.ac.be
Last modification: Aug. 20, 1997, 10:00am.
BSD license

http://www.mathworks.com/matlabcentral/fileexchange/69
Translated from adsgn.m to Python 2009-07-14 endolith@gmail.com
"""

import numpy
from scipy.signal import bilinear


def A_weighting(fs):
    """Design of an A-weighting filter.

    b, a = A_weighting(fs) designs a digital A-weighting filter for
    sampling frequency `fs`. Usage: y = scipy.signal.lfilter(b, a, x).
    Warning: `fs` should normally be higher than 20 kHz. For example,
    fs = 48000 yields a class 1-compliant filter.

    References:
       [1] IEC/CD 1672: Electroacoustics-Sound Level Meters, Nov. 1996.

    """
    # Definition of analog A-weighting filter according to IEC/CD 1672.
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997

    NUMs = [(2*numpy.pi * f4)**2 * (10**(A1000/20)), 0, 0, 0, 0]
    DENs = numpy.polymul([1, 4*numpy.pi * f4, (2*numpy.pi * f4)**2],
                   [1, 4*numpy.pi * f1, (2*numpy.pi * f1)**2])
    DENs = numpy.polymul(numpy.polymul(DENs, [1, 2*numpy.pi * f3]),
                                 [1, 2*numpy.pi * f2])

    # Use the bilinear transformation to get the digital filter.
    # (Octave, MATLAB, and PyLab disagree about Fs vs 1/Fs)
    return bilinear(NUMs, DENs, fs)



def rms_flat(a):  # from matplotlib.mlab
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return numpy.sqrt(numpy.mean(numpy.absolute(a)**2))
