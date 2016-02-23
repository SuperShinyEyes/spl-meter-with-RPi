# Raspberry Pi SPL meter
Sound Pressur Level meter with RPI implemented with Python.
Author: Seyoung Park
E-mail: seyoung.arts.park@protonmail.com
Date: 2016 Feb. 23rd

## Demo

[![demo](/images/demo.png)](https://youtu.be/jp1AkBDQ-8k)

## Requirements
### HW
* Raspberry Pi(1 or 2)
* Microphone (Webcam)

### SW
* Python 2
* EasyProcess==0.2.2
* numpy==1.10.4
* PyAudio==0.2.9
* PyVirtualDisplay==0.1.5
* scipy==0.17.0
* selenium==2.52.0
* wheel==0.24.0

## Filter: A-weighting
I applied A-weighting to filter to filter the stream. A-weighting results frequencies which average person can hear. For further information read: [Frequency Weightings - A-Weighted, C-Weighted or Z-Weighted?](https://www.noisemeters.com/help/faq/frequency-weighting.asp)
For the actual programmatic implementation I borrowed the code from [endolith](https://gist.github.com/endolith/148112) and is saved as /spl_lib.py. A-weighting() is translated from [MATLAB script](: http://www.mathworks.com/matlabcentral/fileexchange/69).
