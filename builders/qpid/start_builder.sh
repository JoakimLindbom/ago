#!/usr/bin/env bash

#Start Docker container. Local catalogue /home/dev is mapped as persistent storage. Change to whatever you like
docker run --volume /home/dev/qpid:/home/dev/qpid -it build:arm
