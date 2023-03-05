FROM alpine:latest

COPY *go* /src/
RUN ['go','build','/src/']

CMD ['/src/TNP-trips']