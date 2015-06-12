import pyaudio
import wave
import sys
import spl_lib as spl 
from scipy.signal import lfilter
import numpy

## The following is similar to a basic CD quality
CHUNK = 4096   # This is the sample size
               # math.pow(2, 12) => RATE / CHUNK = 100ms = 0.1 sec
FORMAT = pyaudio.paInt16    # 16 bit
CHANNEL = 1    # 1 means mono. If stereo, put 2
RATE = 44100   # Logitech HD 720p has rate 44800Hz

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
        # read() returns string. You need to decode it into an array later.
        block = stream.read(CHUNK)
    except IOError, e:
        error_count += 1
        print(" (%d) Error recording: %s" % (errorcount, e))

    decoded_block = numpy.fromstring(block, 'Int16')
    y = lfilter(numerator, denominator, decoded_block)
    decibel = 20*numpy.log10(spl.rms_flat(y))
    print('A-weighted: {:+.2f} dB'.format(decibel))


stream.stop_stream()
stream.close()
pa.terminate()
