# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest.case import SkipTest

def _check_importer(backend):
    import SiQt
    try:
        import SiQt.QtCore
    except ImportError:
        assert True  # this is normal
    except:
        raise
    try:
        SiQt.use(backend, force=False)
    except ImportError:
        raise SkipTest
    except:
        raise
    import SiQt.QtCore


def test_PyQt4_importer():
    _check_importer('PyQt4')

def test_PyQt5_importer():
    _check_importer('PyQt5')

def test_PySide_importer():
    _check_importer('PySide')

