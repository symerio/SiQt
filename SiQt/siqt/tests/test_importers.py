# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def test_importer():
    import SiQt
    try:
        import SiQt.QtCore
    except ImportError:
        assert True  # this is normal
    except:
        raise
    SiQt.use('PyQt4', force=False)
    import SiQt.QtCore



