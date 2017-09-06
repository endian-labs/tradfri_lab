FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install autoconf git python2.7 libtool make -y
RUN git clone --recursive https://github.com/obgm/libcoap.git
WORKDIR /libcoap
RUN git checkout dtls
RUN git submodule update --init --recursive
RUN ./autogen.sh
RUN ./configure --disable-documentation --disable-shared --without-debug CFLAGS="-D COAP_DEBUG_FD=stderr"
RUN make
RUN make install

COPY tradfri_cycle/tradfri_cycle.py /
CMD python2.7 /tradfri_cycle.py
