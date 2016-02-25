#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy as np

class FileInfoWidget(QtGui.QTreeWidget):

    def __init__(self, main_window, parent = None):
        super(FileInfoWidget, self).__init__(parent)
        #layout = QtGui.QVBoxLayout(self)
        self.setWindowTitle('File information')
        self.setGeometry(QtCore.QRect(100, 100, 500, 800))


        header=QtGui.QTreeWidgetItem(["Parameter","Value"])
        self.setHeaderItem(header) 

        header = QtGui.QTreeWidgetItem(self, ["Header"])
        header.setExpanded(True)
        mdict = main_window.gpr.f
        for key in sorted(mdict):
            val = mdict[key]
            if key == 'Comments':
                val = ''.join(val)
            else:
                val = str(val)
            QtGui.QTreeWidgetItem(header, [key, val])


        trace = QtGui.QTreeWidgetItem(self, ["Trace"])
        trace.setExpanded(True)
        for key in sorted(mdict.data.columns):
            if key in ['TraceData', 'TraceNO', 'TraceTime', 'GephoneOrt',
                    'Distance', 'CDPOrt', 'CDPNo', 'EnsembleNo', 'ShotOrt',
                    'TimeDel', 'Timecollect', 'TraceMarker']:
                continue
            val = getattr(mdict.data, key).values
            if key in ['TraceGain', 'ShotNo', 'NoOfSamples', 'IKomp', 'GeophoneNo']:
                val = np.unique(val)

            if len(val) == 1:
                val = val[0]
            QtGui.QTreeWidgetItem(trace, [key, str(val)])


        self.base = main_window
        self.header().resizeSection(0, 230)


    def closeEvent(self, event):
        self.base.widgets['info'] = None
        super(FileInfoWidget, self).closeEvent(event)
