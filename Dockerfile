FROM resin/rpi-raspbian:wheezy-20180411

# Install conda for scientific python
RUN apt-get update && apt-get install -y \
    libportaudio0 \                   # PyAudio dependency
    libportaudio2 \                   # PyAudio dependency
    libportaudiocpp0 \                # PyAudio dependency
    portaudio19-dev \                 # PyAudio dependency
    python-dev \                      # PyAudio dependency
    --no-install-recommends gcc \     # PyAudio dependency
    wget && \
    wget https://repo.continuum.io/miniconda/Miniconda3-3.16.0-Linux-armv7l.sh -O miniconda.sh && \
    apt-get purge wget && \
    bash miniconda.sh -b -p $HOME/miniconda && \ 
    export PATH="$HOME/miniconda/bin:$PATH" && \
    rm miniconda.sh && \
    rm -rf /var/lib/apt/lists/* 

# Install Python packages
#RUN $HOME/miniconda/bin/conda install --yes --file requirements_conda.txt && \
#    $HOME/miniconda/bin/conda install --yes pip && \
#    $HOME/miniconda/bin/pip install -r requirements_pip.txt
#
#
#WORKDIR /app
#ADD . /app