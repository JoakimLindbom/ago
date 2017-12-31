FROM resin/rpi-raspbian:stretch

MAINTAINER Joakim.Lindbom@gmail.com

# Install dependencies
RUN apt update 
RUN apt -qy install apt-utils
RUN apt -qy install quilt \
                    devscripts \
                    libudev-dev \
                    libqpidclient2-dev \
                    uuid-dev \
                    libqpidcommon2-dev \
                    libqpidmessaging2-dev 
RUN apt -qy install git \ 
                    libqpidtypes1-dev \
                    g++ \
                    libtinyxml2-dev \
                    libjsoncpp-dev \
                    libyaml-cpp0.3-dev \
                    libsqlite3-dev 
RUN apt -qy install libi2c-dev \
                    intltool \
                    libboost-dev \
                    libboost-date-time-dev \
                    realpath \
                    libhdate-dev \
                    libcurl4-openssl-dev \
                    liblua5.2-dev 
RUN apt -qy install libola-dev \
                    cmake \
                    libboost-system-dev \
                    libboost-filesystem-dev \
                    libboost-regex-dev \
                    libboost-thread-dev 
RUN apt -qy install libboost-program-options-dev \
                    libaugeas-dev \
                    librrd-dev 
RUN apt -qy install libprocps-dev \
                    libcppdb-dev curl
RUN apt -qy install cmake-curses-gui
RUN apt -qy install build-essential \
                    debhelper
RUN apt -qy install libssl-dev 

#RUN apt -qy install knxd-dev
# (>= 0.10.9) | libeibclient-dev (<= 0.0.5) 

RUN apt -qy install lsb-release 
RUN apt -qy install libopencv-dev \
                    libopencv-core-dev \
                    libopencv-imgproc-dev \
                    libopencv-objdetect-dev \
                    libopencv-highgui-dev

RUN apt -qy install wget 

#Include agocontrol repo
RUN wget http://mirror.at.agocontrol.com/debian/conf/agocontrol.gpg.key
RUN apt-key add agocontrol.gpg.key
RUN echo "deb http://mirror.at.agocontrol.com/raspbian unstable main" >> /etc/apt/sources.list
RUN apt update

# Install from agocontrol repo: Open Z-wave version 1.3. Version 1.4 and 1.5 are available. TODO: Upgrade to 1.5 + regression test
RUN apt -qy install libopenzwave1.3-dev

# Install from agocontrol repo: KNX library missing atm
#RUN apt -qy install libeibclient-dev

#Declare persistent storage. Map this to a local directory when starting this container
ENV BUILD_HOME /home/dev
VOLUME /home/dev

# Build environemnt - git clone needs to e executed after the container is started
# RUN cd "$BUILD_HOME"  \
# && git clone http://git.agocontrol.com/agocontrol/agocontrol.git \
# && cd agocontrol \
# && mkdir build

ENTRYPOINT ["/bin/bash"]

