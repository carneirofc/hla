"""Booster Ramp Control HLA: Ramp Diagnosis Module."""

import numpy as np
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGroupBox, QLabel, QPushButton,\
                           QGridLayout, QSpacerItem, QSizePolicy as QSzPlcy
from pydm.widgets import PyDMWaveformPlot


class Diagnosis(QGroupBox):
    """Widget to ramp status monitoring."""

    def __init__(self, parent=None, prefix='', ramp_config=None):
        """Initialize object."""
        super().__init__('Ramp Diagnosis', parent)
        self.prefix = prefix
        self._wavEff = []
        self._wavXStack = []
        self._wavYStack = []
        self._injcurr_idx = 0
        self._ejecurr_idx = -1
        self._setupUi()

    def _setupUi(self):
        l_boocurr = QLabel('<h4>Booster Current [mA]</h4>', self,
                           alignment=Qt.AlignCenter)
        l_injcurr = QLabel('Injected: ', self, alignment=Qt.AlignRight)
        self.label_injcurr = QLabel(self)
        l_ejecurr = QLabel('Ejected: ', self, alignment=Qt.AlignRight)
        self.label_ejecurr = QLabel(self)

        self.graph_boocurr = PyDMWaveformPlot(self)
        self.graph_boocurr.autoRangeX = True
        self.graph_boocurr.autoRangeY = True
        self.graph_boocurr.backgroundColor = QColor(255, 255, 255)
        self.graph_boocurr.axisColor = QColor(0, 0, 0)
        self.graph_boocurr.showLegend = False
        self.graph_boocurr.showXGrid = True
        self.graph_boocurr.showYGrid = True
        self.graph_boocurr.setLabels(left='Current', bottom='Ramp Index')
        self.graph_boocurr.setStyleSheet("""
            PyDMWaveformPlot{
                min-width:22em;
                min-height:20em;}""")
        self.graph_boocurr.addChannel(
            y_channel=self.prefix+'BO-35D:DI-DCCT:RawReadings-Mon',
            color='blue', lineWidth=2, lineStyle=Qt.SolidLine)
        leftAxis = self.graph_boocurr.getAxis('left')
        leftAxis.setStyle(autoExpandTextSpace=False, tickTextWidth=25)
        self.curveCurrHstr = self.graph_boocurr.curveAtIndex(0)
        self.curveCurrHstr.data_changed.connect(self._updateRampEffGraph)

        l_rampeff = QLabel('<h4>Ramp Efficiency [%]: </h4>', self,
                           alignment=Qt.AlignRight)
        self.label_rampeff = QLabel(self)

        self.graph_rampeff = PyDMWaveformPlot(self)
        self.graph_rampeff.autoRangeX = True
        self.graph_rampeff.autoRangeY = True
        self.graph_rampeff.backgroundColor = QColor(255, 255, 255)
        self.graph_rampeff.axisColor = QColor(0, 0, 0)
        self.graph_rampeff.showLegend = False
        self.graph_rampeff.showXGrid = True
        self.graph_rampeff.showYGrid = True
        self.graph_rampeff.setLabels(
            left='Ramp Efficiency', bottom='Number of cycles')
        self.graph_rampeff.setStyleSheet("""
            PyDMWaveformPlot{
                min-width:22em;
                min-height:20em;}""")
        self.graph_rampeff.addChannel(
            y_channel='FAKE:RampEff-Mon', name='Efficiency',
            color='blue', lineWidth=2, lineStyle=Qt.SolidLine)
        self.graph_rampeff.addChannel(
            y_channel='FAKE:Stacks-Mon', name='Stacks',
            color='red', lineStyle=Qt.NoPen, symbol='o', symbolSize=10)
        leftAxis = self.graph_rampeff.getAxis('left')
        leftAxis.setStyle(autoExpandTextSpace=False, tickTextWidth=25)
        self.curveEff = self.graph_rampeff.curveAtIndex(0)
        self.curveStacks = self.graph_rampeff.curveAtIndex(1)

        self.pb_addStack = QPushButton('Add to stack', self)
        self.pb_addStack.clicked.connect(self._addStack)
        self.pb_addStack.setStyleSheet("""
            min-width:9.68em; max-width:9.68em;""")
        self.pb_addStack.setVisible(False)  # temporary, TODO
        self.pb_clearGraph = QPushButton('Clear graph', self)
        self.pb_clearGraph.clicked.connect(self._clearGraph)
        self.pb_clearGraph.setStyleSheet("""
            min-width:9.68em; max-width:9.68em;""")

        glay = QGridLayout()
        glay.addItem(
            QSpacerItem(20, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 0, 0)
        glay.addWidget(l_boocurr, 1, 1, 1, 2)
        glay.addWidget(l_injcurr, 2, 1)
        glay.addWidget(self.label_injcurr, 2, 2)
        glay.addWidget(l_ejecurr, 3, 1)
        glay.addWidget(self.label_ejecurr, 3, 2)
        glay.addWidget(self.graph_boocurr, 4, 1, 1, 2)
        glay.addItem(
            QSpacerItem(20, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 5, 0)
        glay.addWidget(l_rampeff, 6, 1)
        glay.addWidget(self.label_rampeff, 6, 2)
        glay.addWidget(self.graph_rampeff, 7, 1, 1, 2)
        glay.addWidget(self.pb_addStack, 8, 1)
        glay.addWidget(self.pb_clearGraph, 8, 2)
        glay.addItem(
            QSpacerItem(20, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 9, 3)
        self.setLayout(glay)

    def _updateRampEffGraph(self):
        if self.curveCurrHstr.yData is not None:
            curr_hstr = self.curveCurrHstr.yData
            inj_curr = curr_hstr[self._injcurr_idx]
            eje_curr = curr_hstr[self._ejecurr_idx]
            self._wavEff.append(100*eje_curr/inj_curr)
            if len(self._wavEff) > 1000:
                self._wavEff.pop(0)
            self.label_injcurr.setText(str('{: .8f}'.format(inj_curr)))
            self.label_ejecurr.setText(str('{: .8f}'.format(eje_curr)))
            self.label_rampeff.setText(
                str('{: .8f}'.format(100*eje_curr/inj_curr)))
            self.curveEff.receiveYWaveform(np.array(self._wavEff))
            self.curveEff.redrawCurve()

    def _addStack(self):
        if len(self._wavEff):
            self._wavXStack.append(len(self._wavEff)-1)
            self._wavYStack.append(self._wavEff[-1])
            self.curveStacks.receiveXWaveform(np.array(self._wavXStack))
            self.curveStacks.receiveYWaveform(np.array(self._wavYStack))
            self.curveStacks.redrawCurve()
        # TODO: generate signal to save current BoosterRamp config in a stack

    def _clearGraph(self):
        self._wavXStack.clear()
        self._wavYStack.clear()
        self._wavEff.clear()
        self.curveEff.receiveYWaveform(np.array(self._wavEff))
        self.curveStacks.receiveXWaveform(np.array(self._wavXStack))
        self.curveStacks.receiveYWaveform(np.array(self._wavYStack))
        self.graph_rampeff.redrawPlot()

    def handleUpdateSettings(self, settings):
        """Handle update indeces to calculate ramp efficiency."""
        self._injcurr_idx = settings[0]
        self._ejecurr_idx = settings[1]