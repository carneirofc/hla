from functools import partial as _part
import numpy as np
import time
from qtpy.QtCore import Qt, Slot
from qtpy.QtWidgets import QHBoxLayout, QWidget, QPushButton
import qtawesome as qta
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu
from pydm.widgets import PyDMPushButton
from pydm.widgets.base import PyDMWritableWidget
from pydm.widgets.timeplot import TimePlotCurveItem, PyDMTimePlot, \
    DEFAULT_X_MIN


class RFEnblDsblButton(QWidget):
    """Button to enbl/dsbl attribute controlled by 2 PVs."""

    def __init__(self, parent=None, channels=dict()):
        super().__init__(parent)
        self.pb_off = RFPushButton(
            parent=self, label='Off', init_channel=channels['off'])
        self.pb_off.setStyleSheet('min-width:1.4em; max-width:1.4em;')
        self.pb_on = RFPushButton(
            parent=self, label='On', init_channel=channels['on'])
        self.pb_on.setStyleSheet('min-width:1.4em; max-width:1.4em;')
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(3)
        lay.addWidget(self.pb_off)
        lay.addWidget(self.pb_on)


class RFPushButton(PyDMWritableWidget, QPushButton):

    def __init__(self, parent=None, init_channel=None, label='', icon=None,
                 pressValue=1, releaseValue=0):
        if not icon:
            QPushButton.__init__(self, label, parent)
        else:
            QPushButton.__init__(self, icon, label, parent)
        PyDMWritableWidget.__init__(self, init_channel=init_channel)
        self._alarm_sensitive_border = False
        self.pressValue = pressValue
        self.releaseValue = releaseValue
        self.pressed.connect(_part(self.sendValue, self.pressValue))
        self.released.connect(_part(self.sendValue, self.releaseValue))

    @Slot()
    def sendValue(self, value):
        """Send value."""
        self.send_value_signal[self.channeltype].emit(
            self.channeltype(value))


class MyTimePlotItem(TimePlotCurveItem):
    """Reimplement to do not receive inf values."""

    @Slot(float)
    @Slot(int)
    def receiveNewValue(self, new_value):
        if not np.isinf(new_value):
            super().receiveNewValue(new_value)


class MyTimePlot(PyDMTimePlot):
    """Reimplement to use MyTimePlotItem."""

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self._min_time = time.time()

    def addYChannel(self, y_channel=None, name=None, color=None,
                    lineStyle=None, lineWidth=None, symbol=None,
                    symbolSize=None):
        """Reimplement to use MyTimePlotItem."""
        plot_opts = dict()
        plot_opts['symbol'] = symbol
        if symbolSize is not None:
            plot_opts['symbolSize'] = symbolSize
        if lineStyle is not None:
            plot_opts['lineStyle'] = lineStyle
        if lineWidth is not None:
            plot_opts['lineWidth'] = lineWidth

        # Add curve
        new_curve = MyTimePlotItem(
            y_channel,
            plot_by_timestamps=self._plot_by_timestamps,
            name=name, color=color, **plot_opts)
        new_curve.setUpdatesAsynchronously(self.updatesAsynchronously)
        new_curve.setBufferSize(self._bufferSize)

        self.update_timer.timeout.connect(new_curve.asyncUpdate)
        self.addCurve(new_curve, curve_color=color)

        new_curve.data_changed.connect(self.set_needs_redraw)
        self.redraw_timer.start()

        return new_curve

    def updateXAxis(self, update_immediately=False):
        """Reimplement to show only existing range."""
        if len(self._curves) == 0:
            return

        if self._plot_by_timestamps:
            if self._update_mode == PyDMTimePlot.SynchronousMode:
                maxrange = max([curve.max_x() for curve in self._curves])
            else:
                maxrange = time.time()

            mini = self._min_time
            for curve in self._curves:
                mini = min(mini, curve.data_buffer[0, 0])
            minrange = max(maxrange - self._time_span, mini)

            self.plotItem.setXRange(
                minrange, maxrange, padding=0.0, update=update_immediately)
        else:
            diff_time = self.starting_epoch_time - \
                max([curve.max_x() for curve in self._curves])
            if diff_time > DEFAULT_X_MIN:
                diff_time = DEFAULT_X_MIN
            self.getViewBox().setLimits(minXRange=diff_time)

    def mouseReleaseEvent(self, ev):
        """Reimplement context menu."""
        if ev.button() == Qt.RightButton:
            menu = ViewBoxMenu(self.getViewBox())
            menu.addSeparator()
            rst_act = menu.addAction("Clear buffers")
            rst_act.triggered.connect(self._resetBuffers)
            menu.exec_(self.mapToGlobal(ev.pos()))
        else:
            super().mouseReleaseEvent(ev)

    def _resetBuffers(self):
        for curve in self._curves:
            curve.initialize_buffer()
            self._min_time = time.time()
