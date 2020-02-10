#!/usr/bin/env python-sirius
"""HLA Current and Lifetime Modules."""

import os as _os
import numpy as _np
from qtpy.uic import loadUi
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QHBoxLayout
import qtawesome as qta
from pyqtgraph import ViewBox
from pydm import utilities
from pydm.utilities.macro import substitute_in_file as _substitute_in_file
from pydm.widgets.timeplot import PyDMTimePlot, TimePlotCurveItem
from siriuspy.envars import VACA_PREFIX as _VACA_PREFIX
from siriushla.util import connect_window
from siriushla.widgets import SiriusMainWindow, SiriusConnectionSignal
from siriushla.as_di_dccts import DCCTMain


class CurrLTWindow(SiriusMainWindow):
    """Class to include some intelligence in the .ui file."""

    def __init__(self, parent=None, prefix=_VACA_PREFIX):
        """Initialize some widgets."""
        super(CurrLTWindow, self).__init__(parent)

        UI_FILE = (_os.path.abspath(_os.path.dirname(__file__)) +
                   '/ui_si_ap_currlt.ui')
        tmp_file = _substitute_in_file(UI_FILE, {'PREFIX': prefix})
        self.prefix = prefix
        self.centralwidget = loadUi(tmp_file)
        self.setObjectName('SIApp')
        self.centralwidget.setObjectName('SIApp')
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle('SI Current Info: Current and Lifetime')
        self._setupUi()
        self.setFocus(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def _setupUi(self):
        # set params in widgets in .ui
        self.lifetime_dcct_pv = SiriusConnectionSignal(
            self.prefix+'SI-Glob:AP-CurrInfo:Lifetime-Mon')
        self.lifetime_bpm_pv = SiriusConnectionSignal(
            self.prefix+'SI-Glob:AP-CurrInfo:LifetimeBPM-Mon')
        self.lifetime_dcct_pv.new_value_signal[float].connect(
            self.formatLifetime)
        self.centralwidget.label_lifetime.setText("0:00:00")

        self.centralwidget.DCCT13C4_detail.setObjectName('DCCT13C4_dtl')
        self.centralwidget.DCCT13C4_detail.setStyleSheet(
            "#DCCT13C4_dtl{min-width:25px; max-width:25px; icon-size:20px;}")
        self.centralwidget.DCCT13C4_detail.setIcon(qta.icon('fa5s.ellipsis-h'))
        connect_window(
            self.centralwidget.DCCT13C4_detail, DCCTMain, self,
            prefix=self.prefix, device='SI-13C4:DI-DCCT')
        self.centralwidget.DCCT14C4_detail.setObjectName('DCCT13C4_dtl')
        self.centralwidget.DCCT14C4_detail.setStyleSheet(
            "#DCCT13C4_dtl{min-width:25px; max-width:25px; icon-size:20px;}")
        self.centralwidget.DCCT14C4_detail.setIcon(qta.icon('fa5s.ellipsis-h'))
        connect_window(
            self.centralwidget.DCCT14C4_detail, DCCTMain, self,
            prefix=self.prefix, device='SI-14C4:DI-DCCT')

        self.centralwidget.BufferSize.channel = \
            self.prefix+'SI-Glob:AP-CurrInfo:BuffSize-Mon'
        self.centralwidget.ResetBuffer.setObjectName('reset')
        self.centralwidget.ResetBuffer.setStyleSheet(
            "#reset{min-width:25px; max-width:25px; icon-size:20px;}")
        self.centralwidget.ResetBuffer.setIcon(qta.icon('mdi.delete-empty'))

        self.centralwidget.comboBox_lifetime.currentTextChanged.connect(
            self.handle_lifetime_pv)
        self.centralwidget.spinBox_BuffSize.valueChanged.connect(
            self.setGraphBufferSize)
        self.centralwidget.spinBox_TimeSpan.valueChanged.connect(
            self.setGraphTimeSpan)

        # create graph
        self.graph = MyGraph(self, background='w')
        self.graph.plotItem.getAxis('left').setLabel(
            'Current [mA]', color='blue')
        self.graph.plotItem.getAxis('right').setLabel(
            'Lifetime [h]', color='red')
        self.graph.showLegend = False
        self.graph.showXGrid = True
        self.graph.showYGrid = True
        self.graph.autoRangeY = True
        self.setGraphBufferSize(6000)
        self.setGraphTimeSpan(600)

        self.graph.addYChannel(
            y_channel=self.prefix+'SI-Glob:AP-CurrInfo:Current-Mon',
            axis='left', name='Current', color='blue', lineWidth=2)
        self._curve_current = self.graph.curveAtIndex(0)

        self.graph.addYChannel(
            y_channel='FAKE:Lifetime', axis='right', name='Lifetime',
            color='red', lineWidth=2)
        self._curve_lifetimedcct = self.graph.curveAtIndex(1)

        self.graph.addYChannel(
            y_channel='FAKE:LifetimeBPM', axis='right', name='Lifetime',
            color='red', lineWidth=2)
        self._curve_lifetimebpm = self.graph.curveAtIndex(2)
        self._curve_lifetimebpm.setVisible(False)

        self.lifetime_dcct_pv.new_value_signal[float].connect(
            self._updategraph)
        self.lifetime_bpm_pv.new_value_signal[float].connect(
            self._updategraph)

        self.centralwidget.graphs_wid.setLayout(QHBoxLayout())
        self.centralwidget.graphs_wid.layout().setContentsMargins(0, 0, 0, 0)
        self.centralwidget.graphs_wid.layout().addWidget(self.graph)

    def formatLifetime(self, value):
        """Format lifetime label."""
        lt = value
        if not _np.isnan(lt):
            H = int(lt // 3600)
            m = int((lt % 3600) // 60)
            s = int((lt % 3600) % 60)
            lt_str = '{:d}:{:02d}:{:02d}'.format(H, m, s)
            self.centralwidget.label_lifetime.setText(lt_str)

    @Slot(int)
    def setGraphBufferSize(self, value):
        """Set graph buffer size."""
        self.graph.setBufferSize(value)

    @Slot(int)
    def setGraphTimeSpan(self, value):
        """Set graph time span."""
        self.graph.setTimeSpan(float(value))

    @Slot(str)
    def handle_lifetime_pv(self, text):
        cond = bool(text == 'DCCT')
        self._curve_lifetimedcct.setVisible(cond)
        self._curve_lifetimebpm.setVisible(not cond)
        if not cond:
            self.lifetime_dcct_pv.new_value_signal[float].disconnect(
                self.formatLifetime)
            self.lifetime_bpm_pv.new_value_signal[float].connect(
                self.formatLifetime)
            self.centralwidget.BufferSize.channel = \
                self.prefix+'SI-Glob:AP-CurrInfo:BuffSizeBPM-Mon'
        else:
            self.lifetime_dcct_pv.new_value_signal[float].connect(
                self.formatLifetime)
            self.centralwidget.BufferSize.channel = \
                self.prefix+'SI-Glob:AP-CurrInfo:BuffSize-Mon'
            self.lifetime_bpm_pv.new_value_signal[float].disconnect(
                self.formatLifetime)

    @Slot(float)
    def _updategraph(self, value):
        if 'BPM' in self.sender().address:
            self._curve_lifetimebpm.receiveNewValue(value/3600)
        else:
            self._curve_lifetimedcct.receiveNewValue(value/3600)



class MyGraph(PyDMTimePlot):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.vb2 = ViewBox()
        self.plotItem.scene().addItem(self.vb2)
        self.vb2.setXLink(self.plotItem)
        self.plotItem.getAxis('right').linkToView(self.vb2)
        self.plotItem.showAxis('right')
        self._updateViews()
        self.plotItem.vb.sigResized.connect(self._updateViews)

    def addCurve(self, plot_item, axis='left', curve_color=None):
        if curve_color is None:
            curve_color = utilities.colors.default_colors[
                len(self._curves) % len(utilities.colors.default_colors)]
            plot_item.color_string = curve_color
        self._curves.append(plot_item)
        if axis == 'left':
            self.plotItem.addItem(plot_item)
        elif axis == 'right':
            self.vb2.addItem(plot_item)
        else:
            raise ValueError('Choose a valid axis!')
        self.redraw_timer.start()
        # Connect channels
        for chan in plot_item.channels():
            if chan:
                chan.connect()

    def addYChannel(self, y_channel=None, name=None, color=None,
                    lineStyle=None, lineWidth=None, symbol=None,
                    symbolSize=None, axis='left'):
        """Reimplement addYChannel."""
        plot_opts = dict()
        plot_opts['symbol'] = symbol
        if symbolSize is not None:
            plot_opts['symbolSize'] = symbolSize
        if lineStyle is not None:
            plot_opts['lineStyle'] = lineStyle
        if lineWidth is not None:
            plot_opts['lineWidth'] = lineWidth

        # Add curve
        new_curve = TimePlotCurveItem(
            y_channel,
            plot_by_timestamps=self._plot_by_timestamps,
            name=name, color=color,
            **plot_opts)
        new_curve.setUpdatesAsynchronously(self.updatesAsynchronously)
        new_curve.setBufferSize(self._bufferSize)

        self.update_timer.timeout.connect(new_curve.asyncUpdate)
        self.addCurve(new_curve, axis, curve_color=color)

        new_curve.data_changed.connect(self.set_needs_redraw)
        self.redraw_timer.start()

    def _updateViews(self):
        self.vb2.setGeometry(self.plotItem.vb.sceneBoundingRect())
        self.vb2.linkedViewChanged(self.plotItem.vb, self.vb2.XAxis)
