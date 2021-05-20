ARG BUILD_FROM

FROM alpine:3.13 as builder

RUN apk add --no-cache --virtual .buildDeps \
    build-base \
    libusb-dev \
    librtlsdr-dev \
    cmake \
    git

WORKDIR /build

RUN git clone https://github.com/merbanan/rtl_433
WORKDIR ./rtl_433
ARG rtl433GitRevision=21.05
RUN git checkout ${rtl433GitRevision}
WORKDIR ./build
RUN cmake ..
RUN make -j 4
RUN cat Makefile
WORKDIR /build/root
WORKDIR /build/rtl_433/build
RUN make DESTDIR=/build/root/ install
RUN ls -lah /build/root

FROM $BUILD_FROM

ENV LANG C.UTF-8

ARG rtl433GitRevision=master
LABEL maintainer="georgedot@gmail.com" \
    vcs-ref="${rtl433GitRevision}"

RUN apk add --no-cache libusb librtlsdr
WORKDIR /root
COPY --from=builder /build/root/ /

RUN pip install paho-mqtt
COPY discovery_proxy.py /
RUN chmod a+x /discovery_proxy.py

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
