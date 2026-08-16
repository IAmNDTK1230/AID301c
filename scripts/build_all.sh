#!/usr/bin/env sh
set -eu
python -m src.ingest
python -m src.train
python run_tests.py
