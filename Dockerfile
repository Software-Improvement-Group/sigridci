FROM python:3.11-alpine

RUN apk --no-cache -U upgrade && \
    apk --no-cache add git

COPY sigridci /sigridci
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN git config --system --add safe.directory '*'

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
