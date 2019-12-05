"""Control of EVG Timing Device."""

import sys as _sys
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, \
    QGridLayout, QLabel, QSplitter, QSizePolicy
import qtawesome as qta

from pydm.widgets import PyDMPushButton, PyDMLabel
from siriuspy.csdevice import timesys as _cstime
from siriuspy.search import LLTimeSearch, HLTimeSearch
from siriushla.util import connect_window, get_appropriate_color, \
    connect_newprocess
from siriushla.widgets.windows import create_window_from_widget
from siriushla.widgets import SiriusMainWindow, PyDMLed, PyDMStateButton
from .evg import EventList as _EventList, EVG as _EVG, BucketList
from .evr_eve import EVR as _EVR, EVE as _EVE
from .afc import AFC as _AFC
from .fout import FOUT as _FOUT
from .hl_trigger import HLTriggerList as _HLTriggerList


class TimingMain(SiriusMainWindow):

    def __init__(self, parent=None, prefix=''):
        super().__init__(parent)
        self.prefix = prefix
        self.setupui()
        self.setObjectName('ASApp')
        self.setWindowIcon(
            qta.icon('mdi.timer', color=get_appropriate_color('AS')))

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
        events.setStyleSheet('#events{min-width:30em;}')
        splitter.addWidget(events)

        triggers = self.settriggers()
        triggers.setObjectName('triggers')
        triggers.setStyleSheet('#triggers{min-width:55em;}')
        splitter.addWidget(triggers)

    def setglobalparameters(self):
        wid = QWidget(self.centralWidget())
        wid.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        lay = QGridLayout(wid)

        evg_pref = LLTimeSearch.get_device_names({'dev': 'EVG'})[0]
        evg_pref = self.prefix + evg_pref + ':'
        sp = PyDMPushButton(
            self, init_channel=evg_pref+"UpdateEvt-Cmd", pressValue=1)
        sp.setIcon(qta.icon('fa5s.sync'))
        sp.setToolTip('Update Events Table')
        sp.setObjectName('but')
        sp.setStyleSheet(
            '#but{min-width:25px; max-width:25px; icon-size:20px;}')
        rb = PyDMLed(self, init_channel=evg_pref + "EvtSyncStatus-Mon")
        rb.setOffColor(rb.Red)
        rb.setOnColor(rb.LightGreen)
        lay.addWidget(self._create_prop_widget(
            '<h4>Update Evts</h4>', wid, (sp, rb)), 0, 0)

        sp = PyDMStateButton(self, init_channel=evg_pref + "ContinuousEvt-Sel")
        rb = PyDMLed(self, init_channel=evg_pref + "ContinuousEvt-Sts")
        lay.addWidget(self._create_prop_widget(
            '<h4>Continuous</h4>', wid, (sp, rb)), 0, 1)

        sp = PyDMStateButton(self, init_channel=evg_pref + "InjectionEvt-Sel")
        rb = PyDMLed(self, init_channel=evg_pref + "InjectionEvt-Sts")
        lay.addWidget(self._create_prop_widget(
            '<h4>Injection</h4>', wid, (sp, rb)), 0, 2)

        bucketlist_wid = BucketList(self.centralWidget(), evg_pref)
        lay.addWidget(bucketlist_wid, 0, 3, 2, 1)

        hlay = QHBoxLayout()
        lab = QLabel('Inj Count:', wid)
        pydmlab = PyDMLabel(wid, init_channel=evg_pref+'InjCount-Mon')
        pydmlab.setStyleSheet('min-width:5em;')
        pydmlab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hlay.addStretch()
        hlay.addWidget(lab)
        hlay.addWidget(pydmlab)
        hlay.addStretch()
        pydmlab = PyDMLabel(wid, init_channel=evg_pref+'STATEMACHINE')
        pydmlab.setStyleSheet('min-width:10em;')
        hlay.addWidget(pydmlab)
        hlay.addStretch()
        pydmlab = PyDMLabel(wid, init_channel=evg_pref+'SeqCount-SP')
        pydmlab.rules =\
            '[{"name": "VisibleRule", "property": "Visible", ' +\
            '"expression": "ch[0]==5", "channels": [{"channel": "' +\
            evg_pref + 'STATEMACHINE", "trigger": true}]}]'
        pydmlab.setStyleSheet('min-width:3em;')
        hlay.addWidget(pydmlab)
        hlay.addStretch()
        lay.addItem(hlay, 1, 0, 1, 3)
        return wid

    def setevents(self):
        props = {'name', 'ext_trig', 'mode', 'delay_type', 'delay'}
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
            'detailed', 'status', 'name', 'state', 'source',
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

        icon = qta.icon('mdi.timer', color=get_appropriate_color('AS'))

        menu = main_menu.addMenu('&Devices')
        action = menu.addAction('EVG')
        evg = LLTimeSearch.get_device_names(filters={'dev': 'EVG'})[0]
        Window = create_window_from_widget(_EVG, title=evg, icon=icon)
        connect_window(action, Window, None, prefix=prefix + evg + ':')

        menu_evr = menu.addMenu('EVRs')
        for evr in LLTimeSearch.get_device_names(filters={'dev': 'EVR'}):
            action = menu_evr.addAction(evr)
            Window = create_window_from_widget(_EVR, title=evr, icon=icon)
            connect_window(action, Window, None, prefix=prefix+evr+':')

        menu_eve = menu.addMenu('EVEs')
        for eve in LLTimeSearch.get_device_names(filters={'dev': 'EVE'}):
            action = menu_eve.addAction(eve)
            Window = create_window_from_widget(_EVE, title=eve, icon=icon)
            connect_window(action, Window, None, prefix=prefix + eve + ':')

        menu_afc = menu.addMenu('AMCs')
        for afc in LLTimeSearch.get_device_names(
                                    filters={'dev': 'AMCFPGAEVR'}):
            action = menu_afc.addAction(afc)
            Window = create_window_from_widget(_AFC, title=afc, icon=icon)
            connect_window(action, Window, None, prefix=prefix+afc+':')

        menu_fout = menu.addMenu('Fouts')
        for fout in LLTimeSearch.get_device_names(filters={'dev': 'Fout'}):
            action = menu_fout.addAction(fout)
            Window = create_window_from_widget(_FOUT, title=fout, icon=icon)
            connect_window(action, Window, None, prefix=prefix+fout+':')

        action = main_menu.addAction('&Summary')
        connect_newprocess(
            action, ['sirius-hla-as-ti-control.py', '-t', 'summary'],
            parent=self, is_window=True)

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
