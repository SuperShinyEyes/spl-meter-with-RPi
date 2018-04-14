#FROM shinyeyes/raspbian-miniconda3:latest
#FROM spl-meter-pyaudio-dependencies:latest
FROM spl-meter-conda:latest

WORKDIR /app

ADD . /app

#RUN apt-get update 

# PyAudio dependency
#RUN apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev python-dev && \
#     apt-get install -y --no-install-recommends gcc

# Install Python packages
#RUN $HOME/miniconda/bin/conda install --yes --file requirements_conda.txt
#RUN $HOME/miniconda/bin/conda create --name spl-meter --file requirements_conda.txt
#RUN $HOME/miniconda/bin/conda create --name spl-meter python

#RUN . $HOME/miniconda/bin/activate $HOME/miniconda/envs/spl-meter

RUN $HOME/miniconda/envs/spl-meter/bin/pip install --upgrade pip && \
    $HOME/miniconda/envs/spl-meter/bin/pip install -r requirements_pip.txt

#CMD python spl_meter_text.py 
#CMD $HOME/miniconda/bin/python spl_meter_text.py 
