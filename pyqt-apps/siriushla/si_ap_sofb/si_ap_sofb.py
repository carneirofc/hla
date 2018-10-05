"""Main module of the Application Interface."""

import sys as _sys
import os as _os
from qtpy.QtCore import Qt, QSize, QRect
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QWidget, QDockWidget, QSizePolicy, QVBoxLayout, \
    QPushButton, QTabWidget, QHBoxLayout, QMenu, QMenuBar, \
    QAction, QStatusBar
from siriushla.widgets import SiriusMainWindow
from siriuspy.envars import vaca_prefix as LL_PREF
from siriushla.widgets import PyDMLogLabel
from siriushla.sirius_application import SiriusApplication
from siriushla.si_ap_sofb.orbit_register import OrbitRegisters
from siriushla.si_ap_sofb.graphics import OrbitWidget, \
                                                    CorrectorsWidget
from siriushla.si_ap_sofb.sofb_controllers import ControlSOFB

_dir = _os.path.dirname(_os.path.abspath(__file__))
UI_FILE = _os.path.sep.join([_dir, 'SOFBMain.ui'])


class MainWindow(SiriusMainWindow):
    def __init__(self, prefix, acc='SI'):
        super().__init__()
        self.prefix = prefix
        self.acc = acc
        self.setupui()

    def setupui(self):
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Slow Orbit Feedback System")
        self.resize(2590, 1856)
        self.setDocumentMode(False)
        self.setDockNestingEnabled(True)

        logwid = self._create_log_docwidget()
        orbreg = self._create_orbit_registers()
        wid = self._create_ioc_controllers()

        self.addDockWidget(Qt.DockWidgetArea(1), logwid)
        self.addDockWidget(Qt.DockWidgetArea(2), orbreg)
        self.addDockWidget(Qt.DockWidgetArea(2), wid)

        mwid = self._create_central_widget()
        self.setCentralWidget(mwid)

        self._create_menus()

    def _create_central_widget(self):
        mwid = QWidget(self)
        hbl = QHBoxLayout(mwid)
        hbl.setContentsMargins(0, 0, 0, 0)

        tabwidget = QTabWidget(mwid)
        tabwidget.setMinimumSize(QSize(120, 0))
        tabwidget.setCursor(QCursor(Qt.ArrowCursor))
        tabwidget.setTabShape(QTabWidget.Triangular)
        tabwidget.setElideMode(Qt.ElideNone)
        tabwidget.setTabBarAutoHide(False)
        hbl.addWidget(tabwidget)

        ctrls = self.orb_regtr.get_registers_control()
        chans, ctr = OrbitWidget.get_default_ctrls(self.prefix)
        self._channels = chans
        ctrls.update(ctr)
        orb_wid = OrbitWidget(self, self.prefix, ctrls, self.acc)
        tabwidget.addTab(orb_wid, 'Orbit')

        corr_wid = CorrectorsWidget(self, self.prefix, acc=self.acc)
        tabwidget.addTab(corr_wid, "Correctors")
        tabwidget.setCurrentIndex(0)
        return mwid

    def _create_orbit_registers(self):
        # Create Context Menus for Registers and
        # assign them to the clicked signal
        wid = QDockWidget(self)
        wid.setWindowTitle("Orbit Registers")
        sz_pol = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz_pol.setHorizontalStretch(0)
        sz_pol.setVerticalStretch(1)
        sz_pol.setHeightForWidth(wid.sizePolicy().hasHeightForWidth())
        wid.setSizePolicy(sz_pol)
        wid.setFloating(False)
        wid.setFeatures(QDockWidget.AllDockWidgetFeatures)
        wid.setAllowedAreas(Qt.AllDockWidgetAreas)

        wid_cont = OrbitRegisters(self, self.prefix, self.acc, 9)
        wid.setWidget(wid_cont)
        self.orb_regtr = wid_cont
        return wid

    def _create_ioc_controllers(self):
        docwid = QDockWidget(self)
        docwid.setWindowTitle("SOFB Control")
        sz_pol = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz_pol.setHorizontalStretch(0)
        sz_pol.setVerticalStretch(1)
        sz_pol.setHeightForWidth(docwid.sizePolicy().hasHeightForWidth())
        docwid.setSizePolicy(sz_pol)
        docwid.setMinimumSize(QSize(350, 788))
        docwid.setFloating(False)
        docwid.setFeatures(QDockWidget.AllDockWidgetFeatures)
        wid2 = QWidget(docwid)
        docwid.setWidget(wid2)

        vbl = QVBoxLayout(wid2)
        ctrls = self.orb_regtr.get_registers_control()
        wid = ControlSOFB(wid2, self.prefix, ctrls, self.acc)
        vbl.addWidget(wid)
        return docwid

    def _create_log_docwidget(self):
        docwid = QDockWidget(self)
        docwid.setWindowTitle('IOC Log')
        sz_pol = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz_pol.setHorizontalStretch(0)
        sz_pol.setVerticalStretch(0)
        sz_pol.setHeightForWidth(docwid.sizePolicy().hasHeightForWidth())
        docwid.setSizePolicy(sz_pol)
        docwid.setFloating(False)
        docwid.setMinimumWidth(400)
        wid_cont = QWidget()
        docwid.setWidget(wid_cont)
        vbl = QVBoxLayout(wid_cont)
        vbl.setContentsMargins(0, 0, 0, 0)
        pdm_log = PyDMLogLabel(wid_cont, init_channel=self.prefix+'Log-Mon')
        pdm_log.setAlternatingRowColors(True)
        pdm_log.maxCount = 2000
        vbl.addWidget(pdm_log)
        pbtn = QPushButton('Clear', wid_cont)
        pbtn.clicked.connect(pdm_log.clear)
        vbl.addWidget(pbtn)
        return docwid

    def _create_menus(self):
        menubar = QMenuBar(self)
        menubar.setGeometry(QRect(0, 0, 2290, 19))
        menuopen = QMenu('Open', menubar)

        self.setMenuBar(menubar)
        action = QAction("Correction &Parameters", self)
        action.setCheckable(True)
        action.setChecked(True)
        action.setEnabled(True)
        action.setVisible(True)
        menuopen.addAction(action)

        action = QAction("IOC &Log", self)
        action.setToolTip("IOC Log")
        action.setCheckable(True)
        action.setChecked(True)
        action.setEnabled(True)
        action.setVisible(True)
        menuopen.addAction(action)

        action = QAction("Orbit &Registers", self)
        action.setCheckable(True)
        action.setChecked(True)
        action.setEnabled(True)
        action.setVisible(True)
        menuopen.addAction(action)

        action = QAction("&Open All", self)
        action.setToolTip("Open all dockable windows")
        action.setShortcut("Alt+O")
        action.setChecked(False)
        action.setEnabled(True)
        action.setVisible(True)
        menuopen.addAction(action)

        action = QAction("&Close All", self)
        action.setShortcut("Alt+C")
        action.setEnabled(True)
        action.setVisible(True)
        menuopen.addAction(action)

        menubar.addAction(menuopen.menuAction())

        statusbar = QStatusBar(self)
        statusbar.setEnabled(True)
        self.setStatusBar(statusbar)


def main(prefix=None):
    """Return Main window of the interface."""
    ll_pref = 'ca://' + (prefix or LL_PREF)
    prefix = ll_pref + 'SI-Glob:AP-SOFB:'
    main_win = MainWindow(prefix, 'SI')
    return main_win


def _main():
    app = SiriusApplication()
    _util.set_style(app)
    main_win = main()
    main_win.show()
    _sys.exit(app.exec_())


if __name__ == '__main__':
    import siriushla.util as _util
    _main()
