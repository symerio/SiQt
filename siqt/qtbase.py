# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import os

valid_backends = ['PyQt4', 'PyQt5', 'PySide']

# need to implement https://www.python.org/dev/peps/pep-0302/

def _normalise_name(name):
    for backend in valid_backends:
        if name.lower() == backend.lower():
            return backend
    else:
        raise ValueError('Backend {} is not supported!'.format(name))

SIQT_BACKEND = 'PyQt4'

if 'SIQT_BACKEND' in os.environ:
    SIQT_BACKEND = os.environ['SIQT_BACKEND']
    SIQT_BACKEND = _normalise_name(SIQT_BACKEND)

if SIQT_BACKEND == 'PyQt4':
    import PyQt4 as PyQt
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4 import Qt
    QtPrintSupport = QtGui
    QtWidgets = QtGui
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
elif SIQT_BACKEND == 'PySide':
    import PySide as PyQt
    from PySide import QtCore
    from PySide import QtGui
    #from PySide import Qt
    QtPrintSupport = QtGui
    QtWidgets = QtGui
    QtCore.pyqtSignal = QtCore.Signal
    QtCore.pyqtSlot = QtCore.Slot
    Qt = QtCore.Qt
elif SIQT_BACKEND == 'PyQt5':
    import PyQt5 as PyQt
    from PyQt5 import Qt
    from PyQt5 import QtCore
    from PyQt5 import QtGui
    from PyQt5 import QtPrintSupport
    from PyQt5 import QtWidgets
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
else:
    raise NotImplementedError('Backend {} is not supported!'.format(SIQT_BACKEND))

