FROM shinyeyes/raspbian-miniconda3:latest

WORKDIR /app

ADD . /app

RUN apt-get update 

# PyAudio dependency
RUN apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev python-dev

# Install Python packages
RUN $HOME/miniconda/bin/conda install --yes --file requirements_conda.txt
RUN RUN pip install -r requirements_pip.txt

CMD $HOME/miniconda/bin/python spl_meter_text.py 
