FROM nvidia/cuda:9.0-base-ubuntu16.04

MAINTAINER Binoy Das <binoyd@amazon.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential \
        cuda-command-line-tools-9-0 \
        cuda-cublas-9-0 \
        cuda-cufft-9-0 \
        cuda-curand-9-0 \
        cuda-cusolver-9-0 \
        cuda-cusparse-9-0 \
        libcudnn7=7.0.5.15-1+cuda9.0 \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        libhdf5-dev \
        libcurl3-dev \
        libgtk2.0-0 \
        pkg-config \
        python3-dev \
        python3-pip \
        rsync \
        software-properties-common \
        unzip \
        gzip \
        curl \
        wget \
        vim \
        git \
        nginx \
        ca-certificates \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    find /usr/local/cuda-9.0/lib64/ -type f -name 'lib*_static.a' -not -name 'libcudart_static.a' -delete && \
    rm -rf ~/.nv/


RUN pip3 install --upgrade pip

RUN pip3 --no-cache-dir install \
        setuptools

RUN pip3 --no-cache-dir install \
        tensorflow-gpu==1.6.0

RUN pip3 --no-cache-dir install \
        keras \
        h5py \
        numpy \
        pandas \
        scipy \
        sklearn \
        pyyaml \
        pytz

RUN pip3 --no-cache-dir install \
        flask \
        gevent \
        gunicorn

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY byoa /opt/program
WORKDIR /opt/program
