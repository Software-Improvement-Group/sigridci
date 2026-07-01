# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment setup

- Python 3.9+
- Install test dependencies: `pip3 install -r test/requirements.txt --user`

## Commands

- Run unit tests: `python3 -m unittest`

## Portability

Sigrid CI is used across a variety of enterprise environments. Some people use the Docker container, other people
run the code natively. This makes portability the top concern:

- Do not update the required Python version. We need to be very conservative to ensure portability.
- Do not depend on libraries in production code. 
- It's OK to depend on libraries in test code.

## Architecture

- Sigrid CI consists of a single Python package that people run from the command line, either via Docker or natively.
- The package is located in the `sigridci/sigridci` directory.
- There are two entry point scripts for using the package:
  - `sigridci.py` is the "normal" entry point for interacting with Sigrid.
  - `sigridci_feedback.py` is a special entry point for on-premise Sigrid.
- The sub-package `sigridci.reports` contains all feedback. Everything that produces output to the user is
  referred to as a "report". Command line output is considered a report, Markdown feedback communicated via a
  GitHub pull request comment is also considered a report.
- The sub-package `sigridci.analysisresults` is for parsing the analysis results received from Sigrid. 

## Code style

- Follow PEP-8, but use camelCase for variable names and function names. PEP-8 makes an exception that this is 
  allowed if it is already the dominant style in the project.
- Do not use type hints. We require compatibility with old Python versions, and many additions to the type hint
  system require newer Python versions.
