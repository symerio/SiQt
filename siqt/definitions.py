# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

from .qtbase import QtCore
from .qtbase import QtGui
from .qtbase import QtWidgets

from .dep_resolv import dependency_graph, calculate_dependencies

try:
    from .qtbase.QtCore import QString
except ImportError:
    QString = str



# The following functions are helper functions to setup the GUI
def add_actions(self, target, actions):
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)


def create_action(self, text, slot=None, shortcut=None, 
                    icon=None, tip=None, checkable=False, 
                    signal="triggered"):
    action = QtWidgets.QAction(text, self)
    if icon is not None:
        action.setIcon(QtWidgets.QIcon(":/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        getattr(action, signal).connect(slot)
    if checkable:
        action.setCheckable(True)
    return action

def menu_generator(self, name, label, elements, element_order):
    # File menu
    self.menu[name] = self.menuBar().addMenu("&"+label)
    self.menu[name].elmts = elements

    def show_menu(action):
        def f(value):
            if value:
                action.setDisabled(False)
                action.setEnabled(True)
            else:
                action.setDisabled(True)
                action.setEnabled(False)

        return f

    idx = 1
    for key in element_order:
        if key is None:
            self.menu[name].addSeparator()
            continue


        pars = self.menu[name].elmts[key]

        
        if name == 'view':
            pars['slot'] = self.on_view_handler(key)
            if idx < 10:
                pars['shortcut'] = 'Ctrl+{}'.format(idx)

        if 'slot' not in pars:
            pars['slot'] = getattr(self, 'on_'+key)

        tpars = pars.copy()
        for tkey in ['depends', 'enabled']:
            if tkey in tpars: 
                del tpars[tkey]
        action = self.create_action(**tpars)
        if pars['depends']:  # has some dependecies meaning can't be used initially
            action.setDisabled(True)

        if 'enabled' in pars and not pars['enabled']: 
            action.setDisabled(True)
        self.menu[name].addAction(action)

        pars['qtobject'] = action
        pars['show'] = show_menu(action)
        idx += 1


def set_dep_flag_recursive(self, key, value, sync=False):
    """
    Change status for a dependent field, and pull all the fields that are dependent on it.
    """
    self.dep_flags[key] = value
    for dkey in dependency_graph(key, self.dep_graph):
        self.dep_flags[dkey] = False
    if sync:
        calculate_dependencies(self)


class SiqtElement(dict):

    def __init__(self, qtobj, layout=None, position=None, depends=[], dtype=str, **args):
        """
        A helper class to work with the underlying QtObject
        """
        if isinstance(qtobj, six.string_types):
            qtobj = QtWidgets.QLabel(qtobj)  # if given a string, this is probably a label
        self.dtype = dtype
        super(SiqtElement, self).__init__(qtobj=qtobj, depends=depends, **args)
        if layout is not None and position is not None:
            layout.addWidget(qtobj, *position)

    def set_text(self, value):
        value = QString(str(value))
        self['qtobj'].setText(value)

    @property
    def value(self):
        if isinstance(self['qtobj'], QtWidgets.QCheckBox):
            return self['qtobj'].isChecked()
        elif isinstance(self['qtobj'], QtWidgets.QComboBox):
            key = str(self['qtobj'].currentText())
            return self['choices'][key]
        elif isinstance(self['qtobj'], QtWidgets.QSlider):
            return self.dtype(self['qtobj'].value())
        else:
            val = str(self['qtobj'].text())
            if not val and self.dtype != str:
                val = 0
            return self.dtype(val)

    def __getattr__(self, name):
        """ Only called if name not in the registered methods
        In this case call the qtobject methods """

        return getattr(self['qtobj'],  name)






