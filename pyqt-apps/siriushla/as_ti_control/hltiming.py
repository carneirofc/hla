"""Control of EVG Timing Device."""

import sys as _sys
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, \
    QGridLayout, QGroupBox, QLabel, QSplitter, QSizePolicy
from pydm.widgets import PyDMPushButton
from siriuspy.csdevice import timesys as _cstime
from siriuspy.search import LLTimeSearch, HLTimeSearch
from siriushla.util import connect_window
from siriushla.widgets.windows import create_window_from_widget
from siriushla.widgets import SiriusMainWindow, PyDMLed, PyDMStateButton
from .evg import EventList as _EventList, EVG as _EVG
from .evr_eve import EVR as _EVR, EVE as _EVE
from .afc import AFC as _AFC
from .fout import FOUT as _FOUT
from .hl_trigger import HLTriggerList as _HLTriggerList
from .summary import Summary as _Summary


class TimingMain(SiriusMainWindow):

    def __init__(self, parent=None, prefix=''):
        super().__init__(parent)
        self.prefix = prefix
        self.setupui()
        self.setObjectName('ASApp')

    def setupui(self):
        self.setupmenus()

        mainwid = QWidget(self)
        self.setCentralWidget(mainwid)
        gridlayout = QGridLayout(mainwid)
        gridlayout.setHorizontalSpacing(20)
        gridlayout.setVerticalSpacing(20)

        globpars = self.setglobalparameters()
        gridlayout.addWidget(globpars, 0, 0, 1, 2)

        splitter = QSplitter(Qt.Horizontal)
        gridlayout.addWidget(splitter, 1, 0, 1, 2)
        events = self.setevents()
        events.setObjectName('events')
        splitter.addWidget(events)

        triggers = self.settriggers()
        triggers.setObjectName('triggers')
        splitter.addWidget(triggers)

    def setglobalparameters(self):
        wid = QGroupBox(self.centralWidget())
        wid.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        hbl = QHBoxLayout(wid)

        evg_pref = LLTimeSearch.get_device_names({'dev': 'EVG'})[0]
        evg_pref = self.prefix + evg_pref + ':'
        sp = PyDMPushButton(
            self, init_channel=evg_pref+"UpdateEvt-Cmd", pressValue=1,
            label='Update')
        rb = PyDMLed(self, init_channel=evg_pref + "EvtSyncStatus-Mon")
        hbl.addWidget(self._create_prop_widget(
            '<h4>Update Evts</h4>', wid, (sp, rb)))

        sp = PyDMStateButton(self, init_channel=evg_pref + "ContinuousEvt-Sel")
        rb = PyDMLed(self, init_channel=evg_pref + "ContinuousEvt-Sts")
        hbl.addWidget(self._create_prop_widget(
            '<h4>Continuous</h4>', wid, (sp, rb)))

        sp = PyDMStateButton(self, init_channel=evg_pref + "InjectionEvt-Sel")
        rb = PyDMLed(self, init_channel=evg_pref + "InjectionEvt-Sts")
        hbl.addWidget(self._create_prop_widget(
            '<h4>Injection</h4>', wid, (sp, rb)))
        return wid

    def setevents(self):
        props = {'ext_trig', 'mode', 'delay_type', 'delay'}
        evg_pref = LLTimeSearch.get_device_names({'dev': 'EVG'})[0] + ':'
        names = list(map(
            lambda x: evg_pref + x[1],
            sorted(_cstime.Const.EvtLL2HLMap.items())))
        names = [x for x in names if not x.endswith(('Dsbl', 'PsMtn'))]
        evts = _EventList(
            name='High Level Events', parent=self, prefix=self.prefix,
            props=props, obj_names=names)
        return evts

    def settriggers(self):
        props = {
            'detailed', 'status', 'state', 'source',
            'pulses', 'duration', 'delay'}
        names = HLTimeSearch.get_hl_triggers()
        trigs = _HLTriggerList(
            name='High Level Triggers', parent=self, prefix=self.prefix,
            props=props, obj_names=names)
        return trigs

    def setupmenus(self):
        prefix = self.prefix
        main_menu = self.menuBar()
        main_menu.setNativeMenuBar(False)
        menu = main_menu.addMenu('&Devices')
        action = menu.addAction('EVG')
        evg = LLTimeSearch.get_device_names(filters={'dev': 'EVG'})[0]
        Window = create_window_from_widget(_EVG, title=evg)
        connect_window(action, Window, None, prefix=prefix + evg + ':')

        menu_evr = menu.addMenu('EVRs')
        for evr in LLTimeSearch.get_device_names(filters={'dev': 'EVR'}):
            action = menu_evr.addAction(evr)
            Window = create_window_from_widget(_EVR, title=evr)
            connect_window(action, Window, None, prefix=prefix+evr+':')

        menu_eve = menu.addMenu('EVEs')
        for eve in LLTimeSearch.get_device_names(filters={'dev': 'EVE'}):
            action = menu_eve.addAction(eve)
            Window = create_window_from_widget(_EVE, title=eve)
            connect_window(action, Window, None, prefix=prefix + eve + ':')

        menu_afc = menu.addMenu('AMCs')
        for afc in LLTimeSearch.get_device_names(
                                    filters={'dev': 'AMCFPGAEVR'}):
            action = menu_afc.addAction(afc)
            Window = create_window_from_widget(_AFC, title=afc)
            connect_window(action, Window, None, prefix=prefix+afc+':')

        menu_fout = menu.addMenu('Fouts')
        for fout in LLTimeSearch.get_device_names(filters={'dev': 'Fout'}):
            action = menu_fout.addAction(fout)
            Window = create_window_from_widget(_FOUT, title=fout)
            connect_window(action, Window, None, prefix=prefix+fout+':')

        action = main_menu.addAction('&Summary')
        Window = create_window_from_widget(_Summary, title='Timing Summary')
        connect_window(action, Window, None, prefix=self.prefix)

    def _create_prop_widget(self, name, parent, wids, align_ver=True):
        pwid = QWidget(parent)
        vbl = QVBoxLayout(pwid)
        lab = QLabel(name)
        lab.setAlignment(Qt.AlignCenter)
        vbl.addWidget(lab)
        hbl = QHBoxLayout()
        hbl.setAlignment(Qt.AlignCenter)
        vbl.addItem(hbl)
        for wid in wids:
            wid.setParent(pwid)
            hbl.addWidget(wid)
        return pwid


if __name__ == '__main__':
    """Run Example."""
    from siriuspy.envars import vaca_prefix as PREFIX
    from siriushla.sirius_application import SiriusApplication
    app = SiriusApplication()
    HLTiming = TimingMain(prefix=PREFIX)
    HLTiming.show()
    _sys.exit(app.exec_())
