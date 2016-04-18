#!/bin/bash

if [[ $SIQT_BACKEND == 'PyQt4' ]]; then 
    if [[ ${TRAVIS_PYTHON_VERSION:0:1} == 2 ]]; then
        conda install --yes "PyQT=4.11"
    else
        conda install --yes -c https://conda.anaconda.org/dsdale24 pyqt5
    fi
elif  [[ $SIQT_BACKEND == 'PyQt4' ]]; then
    if [[ ${TRAVIS_PYTHON_VERSION:0:1} == 2 ]]; then
        conda install --yes "pyside"
    else
        conda install --yes -c pyzo pyzo-pyside
    fi
fi
