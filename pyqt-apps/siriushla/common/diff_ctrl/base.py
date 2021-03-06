#!/usr/bin/env python-sirius
"""Scraper and Slit Monitor Base class."""

import os as _os
from qtpy.uic import loadUi
from qtpy.QtCore import Qt, QEvent
from qtpy.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, \
    QLabel, QGridLayout, QSpacerItem, QSizePolicy as QSzPlcy
import qtawesome as qta
from pydm.utilities.macro import substitute_in_file as _substitute_in_file
from pydm.widgets import PyDMSpinbox, PyDMLabel, PyDMPushButton
from siriuspy.envars import VACA_PREFIX as _VACA_PREFIX
from siriuspy.namesys import SiriusPVName as _PVName
from siriushla.widgets import PyDMLedMultiChannel
from siriushla import util
from .details import DiffCtrlDetails as _DiffCtrlDetails


class DiffCtrlDevMonitor(QWidget):
    """Diff Ctrl Dev Monitor Widget."""

    def __init__(self, parent=None, prefix='', device=''):
        """Init."""
        super(DiffCtrlDevMonitor, self).__init__(parent)
        if not prefix:
            self.prefix = _VACA_PREFIX
        else:
            self.prefix = prefix
        self.device = _PVName(device)
        self.section = self.device.sec
        self.orientation = self.device.dev[-1]
        self.setObjectName(self.section+'App')
        self._setupUi()
        self._createConnectors()
        self._setupControlWidgets()
        self.updateDevWidget()

        self.setStyleSheet("""
            PyDMSpinbox, PyDMLabel{
                min-width:5em; max-width: 5em;
            }""")

    def _setupUi(self):
        # status
        label_status = QLabel(
            'Status: ', self, alignment=Qt.AlignRight | Qt.AlignVCenter)
        channels2values = {self.device+':ForceComplete-Mon': 1,
                           self.device+':NegativeDoneMov-Mon': 1,
                           self.device+':PositiveDoneMov-Mon': 1}
        self.multiled_status = PyDMLedMultiChannel(self, channels2values)
        self.multiled_status.setStyleSheet('max-width: 1.29em;')

        self.pb_details = QPushButton(qta.icon('fa5s.ellipsis-h'), '', self)
        self.pb_details.setToolTip('Open details')
        self.pb_details.setObjectName('detail')
        self.pb_details.setStyleSheet(
            "#detail{min-width:25px; max-width:25px; icon-size:20px;}")
        util.connect_window(self.pb_details, _DiffCtrlDetails, parent=self,
                            prefix=self.prefix, device=self.device)

        self.lb_descCtrl1 = QLabel(
            '', self, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.sb_Ctrl1 = PyDMSpinbox(self)
        self.sb_Ctrl1.showStepExponent = False
        self.lb_Ctrl1 = PyDMLabel(self)
        self.lb_descCtrl2 = QLabel(
            '', self, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.sb_Ctrl2 = PyDMSpinbox(self)
        self.sb_Ctrl2.showStepExponent = False
        self.lb_Ctrl2 = PyDMLabel(self)

        self.pb_open = PyDMPushButton(
            parent=self, label='Open', pressValue=1,
            init_channel=self.device+':Home-Cmd')

        tmp_file = _substitute_in_file(
            _os.path.abspath(_os.path.dirname(__file__))+'/ui_as_ap_dev' +
            self.orientation.lower()+'mon.ui', {'PREFIX': self.prefix})
        self.dev_widget = loadUi(tmp_file)

        lay = QGridLayout(self)
        lay.setAlignment(Qt.AlignTop)
        lay.addWidget(label_status, 0, 0)
        lay.addWidget(self.multiled_status, 0, 1)
        lay.addWidget(self.pb_details, 0, 2, alignment=Qt.AlignRight)
        lay.addItem(QSpacerItem(0, 10, QSzPlcy.Ignored, QSzPlcy.Fixed))
        lay.addWidget(self.lb_descCtrl1, 2, 0)
        lay.addWidget(self.sb_Ctrl1, 2, 1)
        lay.addWidget(self.lb_Ctrl1, 2, 2)
        lay.addWidget(self.lb_descCtrl2, 3, 0)
        lay.addWidget(self.sb_Ctrl2, 3, 1)
        lay.addWidget(self.lb_Ctrl2, 3, 2)
        lay.addWidget(self.pb_open, 4, 1, 1, 2)
        lay.addWidget(self.dev_widget, 0, 3, 5, 1)
        lay.addItem(QSpacerItem(0, 10, QSzPlcy.Ignored, QSzPlcy.Fixed))

    def _createConnectors(self):
        """Create connectors to monitor device positions."""
        raise NotImplementedError

    def _setDevPos(self, new_value):
        """Set device widget positions."""
        raise NotImplementedError

    def _setupControlWidgets(self):
        """Setup control widgets channels/labels."""
        raise NotImplementedError

    def updateDevWidget(self):
        """Update device illustration."""
        raise NotImplementedError

    def channels(self):
        """Return channels."""
        raise NotImplementedError


class DiffCtrlView(QWidget):
    """Diff Ctrl View Widget."""

    DEVICE_PREFIX = ''
    DEVICE_CLASS = None

    def __init__(self, parent=None, prefix=''):
        """Init."""
        self.dev_type = 'Slits' if 'Slit' in self.DEVICE_PREFIX else 'Scrapers'
        self.sec = _PVName(self.DEVICE_PREFIX).sec
        super(DiffCtrlView, self).__init__(parent)
        self.setObjectName(self.sec+'App')

        gbox_h = QGroupBox(self.DEVICE_PREFIX + 'H')
        self.dev_h = self.DEVICE_CLASS(self, prefix, self.DEVICE_PREFIX+'H')
        lay_h = QVBoxLayout()
        lay_h.addWidget(self.dev_h)
        gbox_h.setLayout(lay_h)

        gbox_v = QGroupBox(self.DEVICE_PREFIX + 'V')
        self.dev_v = self.DEVICE_CLASS(self, prefix, self.DEVICE_PREFIX+'V')
        lay_v = QVBoxLayout()
        lay_v.addWidget(self.dev_v)
        gbox_v.setLayout(lay_v)

        lay = QVBoxLayout()
        lay.setSpacing(20)
        lay.addWidget(QLabel(
            '<h3>' + self.sec + ' ' +
            ('Slits' if 'Slit' in self.DEVICE_PREFIX else 'Scrapers') +
            ' View</h3>', alignment=Qt.AlignCenter))
        lay.addWidget(gbox_h)
        lay.addWidget(gbox_v)
        self.setLayout(lay)

    def changeEvent(self, event):
        """Reimplement changeEvent."""
        if event.type() == QEvent.FontChange:
            self.dev_h.updateDevWidget()
            self.dev_v.updateDevWidget()
        super().changeEvent(event)
