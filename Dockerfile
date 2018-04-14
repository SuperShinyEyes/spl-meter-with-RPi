FROM resin/rpi-raspbian:latest

WORKDIR /app

ADD . /app

RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y python python-pip --no-install-recommends

# PyAudio dependency
RUN apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev python-dev

RUN pip install -r requirements.txt

