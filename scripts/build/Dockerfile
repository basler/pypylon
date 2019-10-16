ARG QEMU_TARGET_ARCH
ARG DOCKER_BASE_IMAGE

#the following lines are used to get a qemu binary only with docker tools
FROM multiarch/qemu-user-static:4.1.0-1 as qemu

FROM $DOCKER_BASE_IMAGE
COPY --from=qemu /usr/bin/* /usr/bin/


RUN pip install wheel
#build a new swig
RUN mkdir /build && \
    cd /build && \
    wget http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz && \
    tar -xzf swig-3.0.12.tar.gz && cd swig-3.0.12 && \
    ./configure --with-python3 && make -j2 && make install && \
    rm -rf /build

# numpy is required for the pyplon unittests
RUN pip install numpy

# one genicam unittest requires a french locale
RUN apt-get update && apt-get install -y locales \
 && rm -rf /var/lib/apt/lists/* \
 && sed -i 's/^# *\(fr_FR.UTF-8\)/\1/' /etc/locale.gen \
 && locale-gen

RUN mkdir /work
RUN mkdir /pylon_installer

RUN uname -a
