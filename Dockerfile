FROM resin/rpi-raspbian:latest

# Install conda for scientific python and PyAudio Dependencies
RUN apt-get update && apt-get install -y \
    libportaudio0 \                   
#    libportaudio2 \                   
#    libportaudiocpp0 \                
#    portaudio19-dev \                 
#    python-dev \                      
##    --no-install-recommends gcc \     
#    wget && \
#    wget https://repo.continuum.io/miniconda/Miniconda3-3.16.0-Linux-armv7l.sh -O miniconda.sh && \
#    apt-get purge wget && \
#    bash miniconda.sh -b -p $HOME/miniconda && \ 
#    export PATH="$HOME/miniconda/bin:$PATH" && \
#    rm miniconda.sh && \
#    rm -rf /var/lib/apt/lists/* 

# Install Python packages
#RUN $HOME/miniconda/bin/conda install --yes --file requirements_conda.txt && \
#    $HOME/miniconda/bin/conda install --yes pip && \
#    $HOME/miniconda/bin/pip install -r requirements_pip.txt
#
#
#WORKDIR /app
#ADD . /app