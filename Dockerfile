FROM python:3.10-alpine

RUN apk --no-cache -U upgrade && \
    apk --no-cache add git

COPY sigridci /sigridci
ENTRYPOINT ["/sigridci/sigridci.py"]
