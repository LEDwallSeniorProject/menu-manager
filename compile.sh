#!/bin/bash

python -m compileall .
cd demos
python -m compileall .
cd ../games
python -m compileall .
