#!/usr/bin/env python
import pyaudio
import wave
import sys
import spl_lib as spl 
from scipy.signal import lfilter
import numpy

''' The following is similar to a basic CD quality
   When CHUNK size is 4096 it routinely throws an IOError.
   When it is set to 8192 it doesn't.
   IOError happens due to the small CHUNK size
'''
CHUNK = 4800  # This is the sample size
               # math.pow(2, 12) => RATE / CHUNK = 100ms = 0.1 sec
FORMAT = pyaudio.paInt16    # 16 bit
CHANNEL = 1    # 1 means mono. If stereo, put 2
RATE = 48000   # Logitech HD 720p has rate 48000Hz

error_count = 0

numerator, denominator = spl.A_weighting(RATE)

pa = pyaudio.PyAudio()

stream = pa.open(format = FORMAT,
                channels = CHANNEL,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)

print "Listening"

while True:
    try:
        ## read() returns string. You need to decode it into an array later.
        block = stream.read(CHUNK)
    except IOError, e:
        error_count += 1
        print(" (%d) Error recording: %s" % (error_count, e))

    ## Int16 is a numpy data type which is Integer (-32768 to 32767)
    ## If you put Int8 or Int32, the result numbers will be ridiculous
    decoded_block = numpy.fromstring(block, 'Int16')
    ## This is where you apply A-weighted filter
    y = lfilter(numerator, denominator, decoded_block)
    decibel = 20*numpy.log10(spl.rms_flat(y))
    print('A-weighted: {:+.2f} dB'.format(decibel))


stream.stop_stream()
stream.close()
pa.terminate()
