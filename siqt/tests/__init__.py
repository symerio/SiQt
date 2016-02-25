#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from .run_suite import run, run_cli

def get_system_info(pretty_print=False):
    import matplotlib as mpl
    from PyQt4.QtCore import QT_VERSION_STR
    from PyQt4.Qt import PYQT_VERSION_STR
    import platform
    import pandas as pd
    import numpy as np
    system = {}
    for key in ['architecture', 'machine', 'platform', 'processor',
                'system']:
        system[key] = getattr(platform, key)()

    # platform specific stuff
    for key in ['win32_ver', 'mac_ver', 'linux_distribution']:
        res = getattr(platform, key)()
        if res[0]:
            system[key] = res
    if  sys.maxsize > 2**32:
        system['architecture_size'] = '64 bits'
    else:
        system['architecture_size'] = '32 bits'

    python = {}
    for key in [ 'python_implementation', 'python_version', 'python_compiler']:
        python[key] = getattr(platform, key)()

    sv = {}
    sv['numpy'] = np.__version__
    try:
        import scipy
        sv['scipy'] = scipy.__version__
    except ImportError:
        sv['scipy'] = "Not installed"

    sv['pandas'] = pd.__version__
    sv['matplotlib'] = mpl.__version__
    sv['Qt'] = QT_VERSION_STR
    sv['PyQt'] = PYQT_VERSION_STR

    if not pretty_print:
        return {'system': system, 'python': python, 'software_versions': sv}
    else:
        FMT = '   {:12}: {}'
        s = []
        for label, mdict in [('System information', system),
                             ('Python version', python),
                             ('Included modules', sv)]:
            s += ['', label, '='*30, '']
            for key, val in mdict.items():
                if type(val) is tuple:
                    val = ' '.join(val)
                s.append(FMT.format(key, val))
        s.append('')
        

        return '\n'.join(s)
