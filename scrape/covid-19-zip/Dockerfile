FROM alpine:latest

COPY *go* /src
RUN ['go','build','/src']

CMD ['/src/covid-19-zip']