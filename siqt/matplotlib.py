# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .qtbase import SIQT_BACKEND


if SIQT_BACKEND == 'PyQt4':
    PyQtAgg_str = 'Qt4Agg'
else:
    raise NotImplementedError

from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]
