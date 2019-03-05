#!/bin/bash

export PYTHONPATH="$(pwd)/src"
python -m unittest discover -v

