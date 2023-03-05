FROM alpine:latest

RUN ['apt-get','update','&&','apt-get','install','golang','-y']

COPY *go* /src/
WORKDIR /src
RUN ['go','build']

CMD ['/src/taxi-trips']