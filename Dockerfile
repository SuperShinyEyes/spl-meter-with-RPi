FROM shinyeyes/rpi-spl-meter:v0.1

WORKDIR /app

ADD . /app

CMD $HOME/miniconda/envs/spl-meter/bin/python spl_meter_text.py 
