#!/bin/bash

export PYTHONPATH="$(pwd)/src"
python3 -m unittest discover -v

