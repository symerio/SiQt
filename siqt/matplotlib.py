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

