FROM debian:stable-slim
RUN apt-get update -y &&                \
    apt-get upgrade -y --auto-remove

RUN apt-get install -y                  \
    openjdk-25-jre-headless

RUN apt-get install -y                  \
    python3                             \
    python3-pip                         \
    python3-javaproperties              \
    python3-platformdirs                \
    python3-requests-cache

COPY . /usr/local/src/mcme
RUN python3 -m pip install -e /usr/local/src/mcme --break-system-packages
