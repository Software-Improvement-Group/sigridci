FROM python:3.10-alpine

COPY sigridci /sigridci
ENTRYPOINT ["/sigridci/sigridci.py"]
