#!/bin/bash -x
PYTHON_VERSION=$(which python)
echo $PYTHON_VERSION
$PYTHON_VERSION ./setup.py test 
