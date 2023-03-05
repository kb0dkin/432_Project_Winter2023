FROM alpine:latest

COPY *go* /src/
WORKDIR /src
RUN ['go','build']

CMD ['/src/covid-19-zip']