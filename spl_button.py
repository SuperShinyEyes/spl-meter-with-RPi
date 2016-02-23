#!/usr/bin/env python
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

#error_count = 0

numerator, denominator = spl.A_weighting(RATE)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
html_path = os.path.join('file:///', os.path.join(BASE_DIR, 'html/main_button.html')[1:])
single_decibel_file_path = os.path.join(BASE_DIR, 'single_decibel.txt')
max_decibel_file_path = os.path.join(BASE_DIR, 'max_decibel.txt')

def is_meaningful(old, new):
    return abs(old - new) > 3


def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		print "path exists"
		if exception.errno != errno.EEXIST:
			raise


def update_text(path, content):
    #make_sure_path_exists(single_decibel_file_path)
    ## We are only interested down to second decimal
    with open(path, 'w') as f:
        f.write(content)


def refresh():
    driver.get(html_path)

def click(id):
    driver.find_element_by_id(id).click()

def open_html(path):
    driver.get(path)

def check_max(new, max):
    print("check_max called")
    if new > max:
        print("max observed")
        update_text(max_decibel_file_path, 'MAX: {:.2f} dBA'.format(new))
        click('update_max_decibel')
        return new
    else:
        return max


print "Listening"

def listen(old=0, error_count=0, min_decibel=100, max_decibel=0):
    while True:
        try:
            ## read() returns string. You need to decode it into an array later.
            block = stream.read(CHUNK)
        except IOError, e:
            error_count += 1
            print(" (%d) Error recording: %s" % (error_count, e))
        else:
            ## Int16 is a numpy data type which is Integer (-32768 to 32767)
            ## If you put Int8 or Int32, the result numbers will be ridiculous
            decoded_block = numpy.fromstring(block, 'Int16')
            ## This is where you apply A-weighted filter
            y = lfilter(numerator, denominator, decoded_block)
            new_decibel = 20*numpy.log10(spl.rms_flat(y))
            if is_meaningful(old, new_decibel):
                old = new_decibel
                print('A-weighted: {:+.2f} dB'.format(new_decibel))
                update_text(single_decibel_file_path, '{:.2f} dBA'.format(new_decibel))
                max_decibel = check_max(new_decibel, max_decibel)
                #refresh()
                click('update_decibel')


    stream.stop_stream()
    stream.close()
    pa.terminate()



if __name__ == '__main__':
    driver = webdriver.Firefox()
    open_html(html_path)
    listen()
    driver.close()
