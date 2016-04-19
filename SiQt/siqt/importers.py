# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import pkgutil
import os.path

valid_backends = ['PyQt4', 'PyQt5', 'PySide']

def get_path():

    pkg = pkgutil.find_loader('PyQt5')
    return os.path.dirname(pkg.path)

def _normalise_name(name):
    for backend in valid_backends:
        if name.lower() == backend.lower():
            return backend
    else:
        raise ValueError('SiQt backend {} is not supported!\n Must be one of {}'.format(
                            name, valid_backends))

def use(backend_name, force=False, mode='smooth', matplotlib_hook=False):
    """
    Initialize a SiQt backend.

    Parameters
    ----------
     - backend_name: backend name. One of ['PyQt4', 'PyQt5', 'PySide']
     - force: use import hooks to overwrite direct import of the above
       packages by SiQt
     - mode: the import hooks to use
            * "strict": use the backend as it is
            * "smooth": monkeypatch the backend to smooth the differences bewteen
                        backends (e.g. will add SiQt.QtWidgets with the PyQt4 backend,
                        which was only added in PyQt5)
            * "porting": same as smooth, but prints a warning every time an import hook is used.
     - matplotlib_hook: call matplotlib.use with the correct backend
            when matplotlib is first imported
    """
    from .. import this
    name = _normalise_name(backend_name)
    if this.backend is not None:
        print('Warning: SiQt.use(backend_name) should be called before any imports of PyQt.\n'\
                'Calling this a second time will have no effect!')
        return
    this.backend = name
    pkg = pkgutil.find_loader(name)
    path_new = os.path.dirname(pkg.path)
    this.__path__.append(path_new)

