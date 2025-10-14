FROM python:3.13-alpine

RUN apk --no-cache -U upgrade && \
    apk --no-cache add git && \
    git config --system --add safe.directory '*'

COPY sigridci /sigridci

ENTRYPOINT ["/sigridci/sigridci.py"]
