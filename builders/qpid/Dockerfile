FROM resin/rpi-raspbian:stretch

MAINTAINER Joakim.Lindbom@gmail.com

# Install dependencies
RUN apt update 
RUN apt -qy install apt-utils
RUN apt -qy install quilt \
                    devscripts \
                    libudev-dev \
                    uuid-dev 
RUN apt -qy install git cmake libboost-dev uuid-dev pkg-config 
#RUN apt -qy install gcc-c++ 
RUN apt -qy install make ruby help2man doxygen graphviz
RUN apt -qy install build-essential
#                    debhelper

RUN apt -qy install wget 
RUN apt -qy install python2.7
RUN apt -qy install libboost-dev
RUN apt -qy install libboost-all-dev
#ENV BOOST_ROOT /usr/include/boost
RUN apt -qy install python-dev
RUN apt -qy install cmake-curses-gui

#Declare persistent storage. Map this to a local directory when starting this container
ENV BUILD_HOME /home/dev/qpid
VOLUME /home/dev/qpid

# Build environemnt - git clone needs to e executed after the container is started
# RUN cd "$BUILD_HOME"  \
# && git clone http://git.agocontrol.com/agocontrol/agocontrol.git \
# && cd agocontrol \
# && mkdir build

WORKDIR $BUILD_HOME
#RUN git clone https://github.com/apache/qpid-cpp.git

ENTRYPOINT ["/bin/bash"]
