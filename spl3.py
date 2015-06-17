import os, errno
import pyaudio
import spl_lib as spl 
from scipy.signal import lfilter
import numpy

## For web browser handling
from selenium import webdriver

''' The following is similar to a basic CD quality
   When CHUNK size is 4096 it routinely throws an IOError.
   When it is set to 8192 it doesn't.
   IOError happens due to the small CHUNK size
'''
CHUNK = 9600
#CHUNK = 4096  # This is the sample size
               # math.pow(2, 12) => RATE / CHUNK = 100ms = 0.1 sec
FORMAT = pyaudio.paInt16    # 16 bit
CHANNEL = 1    # 1 means mono. If stereo, put 2
#RATE = 44300   # Logitech HD 720p has rate 48000Hz
RATE = 48000

numerator, denominator = spl.A_weighting(RATE)

'''
RPi 2 has a limited cpu power compared to laptops.
Refreshing Firefox demands long time that pyaudio stream get overflowed.
(IOError - Buffer overflow)
Therefore we use multi threads and FIFO Queue to solve this issue.
For Queue read:
https://docs.python.org/2/library/queue.html
For Thread read:

'''
from threading import Thread
from Queue import Full, Queue
chunk_q = Queue(maxsize=3)
decibel_q = Queue(maxsize=3)


'''
Listen to mic
'''
pa = pyaudio.PyAudio()

stream = pa.open(format = FORMAT,
                channels = CHANNEL,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)

'''
Variables related to html(gui)
'''
html_path = 'file:////Users/young/projects/spl_meter/nmain2.html'
#single_decibel_file_path = '/Users/young/projects/spl_meter/single_decibel.txt'
single_decibel_file_path = '/home/pi/spl-meter-with-RPi/single_decibel.txt'

def is_meaningful(old, new):
    return abs(old - new) > 3

def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		print "path exists"
		if exception.errno != errno.EEXIST:
			raise


def update_decibel_text(decibel):
    #make_sure_path_exists(single_decibel_file_path)
    with open(single_decibel_file_path, 'w') as f:
        f.write("%f" % decibel)
        

def refresh():
    driver.get(html_path)
    

print "Listening"

def add_decibel_queue(decibel):
    try:
        decibel_q.put_nowait(new_decibel)
    except Full, e:
        print("decibel queue is full!")
    

def get_decibel(old=0):
    while True:
        if not chunk_q.empty():
            block = chunk_q.get()
            
            ## Int16 is a numpy data type which is Integer (-32768 to 32767)
            ## If you put Int8 or Int32, the result numbers will be ridiculous
            decoded_block = numpy.fromstring(block, 'Int16')

            ## This is where you apply A-weighted filter
            y = lfilter(numerator, denominator, decoded_block)
            new_decibel = 20*numpy.log10(spl.rms_flat(y))
            
            if is_meaningful(old, new_decibel):
                old = new_decibel
                print('A-weighted: {:+.2f} dB'.format(new_decibel))
                update_decibel_text(new_decibel)
                add_decibel_queue(new_decibel)

    

def listen(old=0, error_count=0):
    while True:
        try:
            ## read() returns string. You need to decode it into an array later.
            block = stream.read(CHUNK)
        except IOError, e:
            error_count += 1
            print(" (%d) Error recording: %s" % (error_count, e))
        else:


    stream.stop_stream()
    stream.close()
    pa.terminate()



if __name__ == '__main__':
    driver = webdriver.Firefox()
    chunk_thread = Thread(target=listen)
    chunk_thread.daemon = True
    decibel_thread = Thread(target=get_decibel)
    listen()
    driver.close()
