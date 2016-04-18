#!/bin/bash

if [[ $SIQT_BACKEND == 'PyQt4' ]]; then 
    if [[ ${TRAVIS_PYTHON_VERSION:0:1} == 2 ]]; then
        conda install --yes "PyQT=4.11" $DEPS pip python=${TRAVIS_PYTHON_VERSION}
    elif [[ $TRAVIS_PYTHON_VERSION == "3.4" ]]; then
        conda install -c https://conda.anaconda.org/dsdale24 pyqt5 $DEPS pip python=${TRAVIS_PYTHON_VERSION}
    else  # Python 3.5
        conda install --yes -c https://conda.anaconda.org/mmcauliffe pyqt5 $DEPS pip python=${TRAVIS_PYTHON_VERSION}
    fi
elif  [[ $SIQT_BACKEND == 'PyQt4' ]]; then
    if [[ ${TRAVIS_PYTHON_VERSION:0:1} == 2 ]]; then
        conda install --yes "pyside" $DEPS pip python=${TRAVIS_PYTHON_VERSION}
    else
        conda install --yes -c pyzo pyzo-pyside $DEPS pip python=${TRAVIS_PYTHON_VERSION}
    fi
fi
