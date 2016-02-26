# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .qtbase import SIQT_BACKEND

import matplotlib

if SIQT_BACKEND == 'PyQt4':
    PyQtAgg_str = 'Qt4Agg'
    matplotlib.use(PyQtAgg_str)
    matplotlib.rcParams['backend.qt4'] = SIQT_BACKEND
    import matplotlib.backends.backend_qt4agg as backend_qtagg
elif SIQT_BACKEND == 'PySide':
    PyQtAgg_str = SIQT_BACKEND
    matplotlib.use('Qt4Agg')
    matplotlib.rcParams['backend.qt4'] = SIQT_BACKEND
    import matplotlib.backends.backend_qt4agg as backend_qtagg
elif SIQT_BACKEND == 'PyQt5':
    PyQtAgg_str = 'Qt5Agg'
    matplotlib.use(PyQtAgg_str)
    matplotlib.rcParams['backend.qt5'] = SIQT_BACKEND
    import matplotlib.backends.backend_qt5agg as backend_qtagg
else:
    raise NotImplementedError

class NavigationToolbar(backend_qtagg.NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in backend_qtagg.NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
