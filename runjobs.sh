#!/usr/bin/env bash

source .venv/bin/activate
export FLASK_APP="run.py"
export FLASK_DEBUG=1
flask download-data
flask get-latest-prices
flask process-data