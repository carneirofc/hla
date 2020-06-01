"""PS Graph Monitor."""
import numpy as _np
from epics import PV as _PV

from qtpy.QtCore import Qt, QSize, QTimer
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGridLayout, QWidget, QLabel, QHBoxLayout, \
    QComboBox, QToolTip, QSpacerItem, QSizePolicy as QSzPlcy, QApplication, \
    QGraphicsScene
import qtawesome as qta
from pyqtgraph import mkPen, mkBrush
from pydm.widgets import PyDMWaveformPlot

from siriuspy.envars import VACA_PREFIX as _vaca_prefix
from siriuspy.namesys import SiriusPVName
from siriuspy.search import PSSearch as _PSSearch, \
    MASearch as _MASearch
from siriuspy.pwrsupply.csdev import Const as _PSConst

from siriushla.as_ps_control.PSDetailWindow import PSDetailWindow
from siriushla.widgets import SiriusMainWindow


class PSGraphMon(SiriusMainWindow):
    """Power supply graph monitor."""

    _pvs = dict()

    def __init__(self, parent=None, prefix=_vaca_prefix, filters=''):
        super().__init__(parent)
        self.setWindowTitle('Power Supplies Graph Monitor')
        self._filters = filters
        if not filters:
            self.setObjectName('ASApp')
            filters = {'sec': 'SI', 'dis': 'PS', 'dev': 'CH'}
        else:
            self.setObjectName(filters['sec']+'App')
        self._prefix = prefix
        self._psnames = _PSSearch.get_psnames(filters)
        self._property_line = 'Current-Mon'
        self._property_symb = 'DiagStatus-Mon'

        self._choose_sec = ['TB', 'BO', 'TS', 'SI']

        self._choose_sub = ['All', ]
        self._choose_sub.extend(['{0:02d}.*'.format(i+1) for i in range(20)])
        self._choose_sub.extend(
            ['.*M1', '.*M2', '.*C1', '.*C2', '.*C3', '.*C4'])

        self._choose_dev = {
            sec: ['CH', 'CV', 'C(H|V)'] for sec in self._choose_sec}
        self._choose_dev['SI'].extend(
            ['QS', 'QFA', 'QFB', 'QFP', 'QF.*',
             'QDA', 'QDB1', 'QDB2', 'QDP1', 'QDP2', 'QD.*',
             'Q1', 'Q2', 'Q3', 'Q4', 'Q[1-4]',
             'Q(D|F).*', 'Q(F|D|[1-4]).*'])

        self._choose_prop_symb = {
            'DiagStatus-Mon': 0,
            'IntlkSoft-Mon': 0,
            'IntlkHard-Mon': 0,
            'PwrState-Sel': _PSConst.PwrStateSel.On,
            'PwrState-Sts': _PSConst.PwrStateSts.On,
            'OpMode-Sel': _PSConst.OpMode.SlowRef,
            'OpMode-Sts': _PSConst.States.SlowRef,
            'CtrlMode-Mon': _PSConst.Interface.Remote,
            'CtrlLoop-Sel': _PSConst.OpenLoop.Open,
            'CtrlLoop-Sts': _PSConst.OpenLoop.Open,
            'CycleEnbl-Mon': _PSConst.DsblEnbl.Enbl}
        self._choose_prop_line = [
            'Current-Mon', 'Current-SP', 'Current-RB', 'CurrentRef-Mon',
            'DiagCurrentDiff-Mon', 'WfmSyncPulseCount-Mon',
            'PRUCtrlQueueSize-Mon']

        self._setupUi()

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_graph)
        self._timer.setInterval(250)
        self._timer.start()

    def _setupUi(self):
        aux_label = '' if not self._filters \
            else ' - '+self._filters['sec']+' '+self._filters['dev']
        self._label = QLabel('<h3>PS Graph Monitor'+aux_label+'</h3>',
                             self, alignment=Qt.AlignCenter)

        if not self._filters:
            self._cb_sec = QComboBox(self)
            for item in self._choose_sec:
                self._cb_sec.addItem(item)
            self._cb_sec.setCurrentText('SI')
            self._cb_sec.currentTextChanged.connect(
                self._handle_cb_visibility)
            self._cb_sec.currentTextChanged.connect(
                self._set_psnames)

            self._cb_sub = QComboBox(self)
            self._cb_sub.setEditable(True)
            self._cb_sub.setMaxVisibleItems(10)
            for item in self._choose_sub:
                self._cb_sub.addItem(item)
            self._cb_sub.currentTextChanged.connect(
                self._set_psnames)

            glay_choose = QGridLayout()
            glay_choose.addWidget(self._cb_sub, 0, 0)
            self._cb_dev = dict()
            for sec in self._choose_sec:
                visible = sec == 'SI'

                self._cb_dev[sec] = QComboBox(self)
                self._cb_dev[sec].setMaxVisibleItems(10)
                self._cb_dev[sec].setVisible(visible)
                for item in self._choose_dev[sec]:
                    self._cb_dev[sec].addItem(item)
                self._cb_dev[sec].currentTextChanged.connect(
                    self._set_psnames)

                glay_choose.addWidget(self._cb_dev[sec], 0, 1)

        self._label_symb = QLabel()
        icon = qta.icon('mdi.record-circle-outline')
        pixmap = icon.pixmap(icon.actualSize(QSize(20, 20)))
        self._label_symb.setPixmap(pixmap)
        self._label_symb.setSizePolicy(QSzPlcy.Fixed, QSzPlcy.Fixed)
        self._cb_prop_symb = QComboBox(self)
        self._cb_prop_symb.currentTextChanged.connect(
            self._update_property_symb)
        self._cb_prop_symb.setSizePolicy(QSzPlcy.Expanding, QSzPlcy.Preferred)
        self._cb_prop_symb.setMaxVisibleItems(10)
        for item in self._choose_prop_symb.keys():
            self._cb_prop_symb.addItem(item)
        hbox_prop_symb = QHBoxLayout()
        hbox_prop_symb.addWidget(self._label_symb)
        hbox_prop_symb.addWidget(self._cb_prop_symb)

        self._label_line = QLabel()
        icon = qta.icon('mdi.pulse')
        pixmap = icon.pixmap(icon.actualSize(QSize(20, 20)))
        self._label_line.setPixmap(pixmap)
        self._label_line.setSizePolicy(QSzPlcy.Fixed, QSzPlcy.Fixed)
        self._cb_prop_line = QComboBox(self)
        self._cb_prop_line.currentTextChanged.connect(
            self._update_property_line)
        self._cb_prop_line.setSizePolicy(QSzPlcy.Expanding, QSzPlcy.Preferred)
        self._cb_prop_line.setMaxVisibleItems(10)
        for item in self._choose_prop_line:
            self._cb_prop_line.addItem(item)
        hbox_prop_line = QHBoxLayout()
        hbox_prop_line.addWidget(self._label_line)
        hbox_prop_line.addWidget(self._cb_prop_line)

        self._graph = PSGraph(self)
        self._graph.psnames = self._psnames
        self._create_pvs(self._property_symb)
        self._graph.symbols = self._get_values(self._property_symb)
        self._create_pvs(self._property_line)
        self._graph.y_data = self._get_values(self._property_line)

        cw = QWidget()
        self.setCentralWidget(cw)
        lay = QGridLayout(cw)
        lay.addWidget(self._label, 0, 0, 1, 4)
        lay.addItem(
            QSpacerItem(1, 10, QSzPlcy.Ignored, QSzPlcy.Fixed), 1, 0, 1, 4)
        if not self._filters:
            lay.addWidget(QLabel('Power supply: '), 2, 0)
            lay.addWidget(self._cb_sec, 2, 1)
            lay.addLayout(glay_choose, 2, 2)
            lay.addItem(
                QSpacerItem(1, 1, QSzPlcy.Expanding, QSzPlcy.Ignored), 2, 3)
        lay.addWidget(QLabel('Properties: '), 3, 0)
        lay.addLayout(hbox_prop_symb, 3, 1)
        lay.addLayout(hbox_prop_line, 3, 2)
        lay.addItem(
            QSpacerItem(1, 1, QSzPlcy.Expanding, QSzPlcy.Ignored), 3, 3)
        lay.addItem(
            QSpacerItem(1, 10, QSzPlcy.Ignored, QSzPlcy.Fixed), 4, 0, 1, 4)
        lay.addWidget(self._graph, 5, 0, 1, 4)

        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 2)
        lay.setColumnStretch(2, 2)
        lay.setColumnStretch(3, 5)

    def _set_psnames(self):
        sec = self._cb_sec.currentText()
        if sec == 'SI':
            sub = self._cb_sub.currentText()
            sub = sub if sub != 'All' else '.*'
        else:
            sub = '.*'
        dev = self._cb_dev[sec].currentText()

        self._psnames = _PSSearch.get_psnames(
            {'sec': sec, 'sub': '(?!Fam)'+sub, 'dis': 'PS', 'dev': dev})
        self._update_graph()

    def _handle_cb_visibility(self):
        current_sec = self.sender().currentText()
        self._cb_sub.setVisible(current_sec == 'SI')
        for sec in self._choose_sec:
            self._cb_dev[sec].setVisible(current_sec == sec)

    def _update_property_line(self):
        self._property_line = self._cb_prop_line.currentText()

    def _update_property_symb(self):
        self._property_symb = self._cb_prop_symb.currentText()

    def _update_graph(self):
        self._create_pvs(self._property_line)
        self._create_pvs(self._property_symb)
        self._graph.psnames = self._psnames
        self._graph.symbols = self._get_values(self._property_symb)
        self._graph.y_data = self._get_values(self._property_line)

    # ---------- pv handler methods ----------

    def _create_pvs(self, propty):
        new_pvs = dict()
        for psn in self._psnames:
            pvname = self._prefix+psn+':'+propty
            if pvname in PSGraphMon._pvs:
                continue
            new_pvs[pvname] = _PV(pvname, connection_timeout=0.05)
        PSGraphMon._pvs.update(new_pvs)

    def _get_values(self, propty):
        for psn in self._psnames:
            pvname = self._prefix+psn+':'+propty
            PSGraphMon._pvs[pvname].wait_for_connection()

        values = list()
        for psn in self._psnames:
            pvname = self._prefix+psn+':'+propty
            val = PSGraphMon._pvs[pvname].get()
            val = val if val is not None else 0
            if propty in self._choose_prop_symb.keys():
                defval = self._choose_prop_symb[propty]
                val = 1 if val == defval else 0
            values.append(val)
        return values


class PSGraph(PyDMWaveformPlot):
    """Power supply data graph."""

    def __init__(self, parent=None, psnames=list(), y_data=list(),
                 symbols=list(), color='blue'):
        """Init."""
        super().__init__(parent)
        self.setBackgroundColor(QColor(255, 255, 255))
        self.setAutoRangeX(True)
        self.setAutoRangeY(True)
        self.setShowXGrid(True)
        self.setShowYGrid(True)
        self.setObjectName('graph')
        self.setStyleSheet('#graph{min-width:60em;min-height:12em;}')
        self._nok_pen = mkPen(QColor(color))
        self._nok_brush = mkBrush(QColor(255, 0, 0))
        self._ok_pen = mkPen(QColor(color))
        self._ok_brush = mkBrush(QColor(0, 200, 0))
        self._all_pen = [self._nok_pen, ]
        self._all_brush = [self._nok_brush, ]

        self.addChannel(
            y_channel='Mean', x_channel='Pos', color='black',
            lineStyle=2, lineWidth=2)
        self.mean = self.curveAtIndex(0)

        self.addChannel(
            y_channel='Kicks', x_channel='Pos', color=color,
            lineWidth=2, symbol='o', symbolSize=10)
        self.curve = self.curveAtIndex(1)

        self.psnames = psnames
        self.symbols = symbols
        self.y_data = y_data

        # try to fix bug in pyqtgraph
        self.sceneObj.mouseReleaseEvent = self._sceneObj_mouseReleaseEvent

    @property
    def psnames(self):
        """Return psnames."""
        return self._psnames

    @psnames.setter
    def psnames(self, new):
        if not new:
            self.curve.receiveXWaveform(_np.array([0, ]))
            self.curve.receiveYWaveform(_np.array([0, ]))
            self.mean.receiveXWaveform(_np.array([0, ]))
            self.mean.receiveYWaveform(_np.array([0, ]))
            return

        self._x_data = _np.array(_MASearch.get_mapositions(map(
            lambda x: x.substitute(dis='MA'), new)))
        self._psnames = [psn for _, psn in sorted(zip(self._x_data, new))]
        self._x_data = _np.sort(self._x_data)
        self._tooltips = [psn.get_nickname(dev=True) for psn in self._psnames]

        self._sector = SiriusPVName(new[0]).sec
        if self._sector == 'TB':
            self._c0 = 21.2477
        elif self._sector == 'TS':
            self._c0 = 26.8933
        elif self._sector == 'BO':
            self._c0 = 496.8
        elif self._sector == 'SI':
            self._c0 = 518.396

        self.curve.receiveXWaveform(self._x_data)
        self.mean.receiveXWaveform(self._x_data)

    @property
    def sector(self):
        """Return sector."""
        return self._sector

    @property
    def tooltips(self):
        """Return tooltips."""
        return self._tooltips

    @property
    def x_data(self):
        """Return x_data."""
        return self._x_data

    @property
    def y_data(self):
        """Return y_data."""
        return self._y_data

    @y_data.setter
    def y_data(self, new):
        if not new or any([n is None for n in new]):
            self._y_data = _np.array([0, ])
        else:
            self._y_data = _np.array(new)

        self.curve.receiveYWaveform(self._y_data)
        self.curve.opts['symbolPen'] = self._all_pen
        self.curve.opts['symbolBrush'] = self._all_brush
        self.curve.redrawCurve()

        self.mean.receiveYWaveform(
            _np.array([_np.mean(self._y_data)]*len(self._y_data)))
        self.mean.redrawCurve()

    @property
    def symbols(self):
        """Return symbols."""
        return self._symbols

    @symbols.setter
    def symbols(self, new):
        if not new:
            return
        self._symbols = new
        all_brush, all_pen = [], []
        for sym in self._symbols:
            if sym:
                all_pen.append(self._ok_pen)
                all_brush.append(self._ok_brush)
            else:
                all_pen.append(self._nok_pen)
                all_brush.append(self._nok_brush)
        self._all_pen = all_pen
        self._all_brush = all_brush

    def mouseMoveEvent(self, event):
        """Reimplement mouseMoveEvent."""
        pos = event.pos()
        posx = self.curve.scatter.mapFromScene(pos).x()
        posx = posx % self._c0
        ind = _np.argmin(_np.abs(_np.array(self._x_data)-posx))
        txt = '{0:s}, y = {1:.3f} m'.format(self.tooltips[ind], posx)
        QToolTip.showText(
            self.mapToGlobal(pos), txt, self, self.geometry(), 500)
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        """Reimplement mouseDoubleClickEvent."""
        posx = self.curve.xData
        view = self.plotItem.getViewBox()
        pos = view.mapSceneToView(event.pos())
        idx = _np.argmin(_np.abs(posx-pos.x()))
        psname = self._psnames[idx]
        self._open_ps_detail(psname)
        super().mouseDoubleClickEvent(event)

    def _open_ps_detail(self, psname):
        """Open PSDetailWindow."""
        app = QApplication.instance()
        app.open_window(PSDetailWindow, parent=self, **{'psname': psname})

    def _sceneObj_mouseReleaseEvent(self, event):
        """Copy sceneObj.mouseReleaseEvent and fix bug."""
        sceneObj = self.sceneObj
        if sceneObj.mouseGrabberItem() is None:
            if event.button() in sceneObj.dragButtons:
                if sceneObj.sendDragEvent(event, final=True):
                    event.accept()
                sceneObj.dragButtons.remove(event.button())
            else:
                cev = [e for e in sceneObj.clickEvents
                       if int(e.button()) == int(event.button())]
                if cev:  # change: handle IndexError raised when cev is empty
                    if sceneObj.sendClickEvent(cev[0]):
                        event.accept()
                    sceneObj.clickEvents.remove(cev[0])

        if int(event.buttons()) == 0:
            sceneObj.dragItem = None
            sceneObj.dragButtons = []
            sceneObj.clickEvents = []
            sceneObj.lastDrag = None
        QGraphicsScene.mouseReleaseEvent(sceneObj, event)

        sceneObj.sendHoverEvents(event)