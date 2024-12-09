FROM python:3.11-alpine

RUN apk --no-cache -U upgrade && \
    apk --no-cache add git

COPY sigridci /sigridci
RUN cp /sigridci/gitconfig-add-safe-directory $HOME/.gitconfig

ENTRYPOINT ["/sigridci/sigridci.py"]
