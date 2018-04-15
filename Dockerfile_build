FROM shinyeyes/raspbian-miniconda3:latest

WORKDIR /app

ADD . /app

# PyAudio dependency
RUN apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev python-dev && \
    apt-get install -y --no-install-recommends gcc

# Install Python packages
RUN $HOME/miniconda/bin/conda create --name spl-meter --file requirements_conda.txt

RUN $HOME/miniconda/envs/spl-meter/bin/pip install -r requirements_pip.txt

CMD $HOME/miniconda/envs/spl-meter/bin/python spl_meter_text.py 
