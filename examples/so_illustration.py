# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

import pkgutil
import os.path
import six

valid_backends = ['PyQt5']
redirect_to_backend = 'PyQt4' # can be changed to  to PySide


class RenameImportFinder(object):
    """
    Adapted from https://github.com/PythonCharmers/python-future/blob/master/src/future/standard_library/__init__.py#L232
    """

    def find_module(self, fullname, path=None):
        """ This is the finder function that renames all imports like
             PyQt4.module or PySide.module into PyQt4.module """
        for backend_name in valid_backends:
            if fullname.startswith(backend_name):
                # just rename the import
                name_new = fullname.replace(backend_name, redirect_to_backend)
                print('Renaming import:', fullname, '->', name_new, )
                print('   Path:', path)
                return RenameImportLoader(name_orig=fullname, path=path,
                        name_new=name_new)
        return None

class RenameImportLoader(object):
    """
    Adapted from https://github.com/PythonCharmers/python-future/blob/master/src/future/standard_library/__init__.py#L232
    """
    def __init__(self, name_orig, path, name_new):
        self.name_orig = name_orig
        self.path = path
        self.name_new = name_new

    def load_module(self, name, path=None):
        """ Handles hierarchical importing: package.module.module2
        As far as I understand this should be the default python loader
        since I could not find it, this is adapted from the __init__.py of
                future.standard_library
        """

        # Ignore the provided path and name and use the renamed ones
        if path is None:
            path = self.path
        name = self.name_new
        if name in sys.modules:
            module = sys.modules[name]
        else:
            module = self._find_and_load_module(name, path)
            sys.modules[name] = module
        # overwriting some properties that end up set uncorrectly
        module.__name__ = self.name_new
        module.__package__ = redirect_to_backend
        if six.PY3:
            if module.__spec__ is not None:
                module.__spec__.name = self.name_new
        return module


    def _find_and_load_module(self, name, path=None):
        """
        Finds and loads it. But if there's a . in the name, handles it properly.
        """
        import imp
        bits = name.split('.')
        while len(bits) > 1:
            # Treat the first bit as a package
            packagename = bits.pop(0)
            package = self._find_and_load_module(packagename, path)
            try:
                path = package.__path__
            except AttributeError:
                if name in sys.modules:
                    return sys.modules[name]

        name = bits[0]
        if name in sys.modules:
            module = sys.modules[name]
        else:
            fp, pathname, description = imp.find_module(name, path)
            try:
                module = imp.load_module(self.name_orig, fp, pathname, description)
            finally:
                if fp:
                    fp.close()
        return module


sys.meta_path.insert(0, RenameImportFinder())

if __name__ == '__main__':
    # this should import PyQt4 instead of PyQT5 
    # you don't need to have PyQt5 installed
    import gzip
    import PyQt5
    import PyQt5.QtCore
    print(PyQt5.__name__)                # PyQt4
    print(PyQt5.__package__)             # PyQt4
    print(PyQt5.QtCore.QT_VERSION_STR)   # 4.8.x
