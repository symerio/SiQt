#!/usr/bin/python
# -*- coding: utf-8 -*-
#from PyQt4 import QtCore
from PyQt4 import QtGui

import numpy as np


def show_qt_control_element(el):
    def f(status=False):
        #el.setDisabled(not status)
        el.setEnabled(status)
    return f

def sync_gui(lock=[], update=[], view_mode=None, background=False):
    def decorator_generator(f):
        def f_wrapper(self, *args, **kwargs):
            # lock some elements if need be
            for el in lock:
                p = el(self)
                if 'show' in p:
                    p['show'](False)
                    p['is_visible'] = False
                else:
                    # go one level down, this is a dict of dics
                    for key in p:
                        p[key]['show'](False)
                        p[key]['is_visible'] = False


            for key in update:
                self.set_dep_flag_recursive(key, True)

            QtGui.QApplication.processEvents()

            f(self, *args, **kwargs)

            if view_mode is not None:
                self.view_mode = view_mode
                self.on_draw()
            if not background:
                calculate_dependencies(self, verbose=False)
        return f_wrapper
    return decorator_generator

def dependency_graph(key, storage):
    out = []
    if key in storage:
        fields = storage[key]
        out += fields
        for pkey in fields:
            new_fields = dependency_graph(pkey, storage)
            if new_fields:
                out += new_fields
    return out


def calculate_dependencies(self, verbose=False, initialize=False):
    """
        This function allows to determine which graphical should be active
        depending on the current processing step
    """
    dep_list = []

    for menu_el in self.menu.values():
        for key, el in  menu_el.elmts.items():
            if 'enabled' in el and not el['enabled']:
                continue
            dep_list.append(('menu', key, el))
    for key, el in self.controls.items():
        dep_list.append(('controls', key, el))

    for tab_name, tab_el in self.tabs.items():
        for key, el in  tab_el.items():
            dep_list.append(('tabs', key, el))


    if initialize:
        for tab_name, tab_el in self.tabs.items():
            for key, el in  tab_el.items():
                if 'show' not in el:
                    el['show'] = show_qt_control_element(el['qtobj'])
        for mtype, key, el in dep_list:
            if 'is_visible' not in el:
                el['is_visible'] = None

    for mtype, key, el in dep_list:
        # check if the dependency for this control element is verified
        res = [self.dep_flags[dkey] for dkey in el['depends']]
        if not len(res):
            res = True
        else:
            res = np.array(res).all()
        if verbose:
            print('{:10} {:20} {:10} {:10}'.format(mtype, key, el['is_visible'], str(res)))

        if el['is_visible'] != res:
            try:
                el['show'](res)
            except:
                print(el)
                raise
            el['is_visible'] = res
