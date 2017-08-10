#!/usr/local/bin/python3.6
import sys
from pydm import PyDMApplication
from pydm.PyQt.QtCore import pyqtSlot
from pydm.PyQt.QtGui import QMainWindow, QAction, QMenuBar
from siriushla.as_ps_cycle import PsCycleWindow
from siriushla.as_ma_control import ToBoosterMagnetControlWindow
from siriushla.as_ma_control import BoosterMagnetControlWindow
from siriushla.as_ma_control import ToSiriusMagnetControlWindow
from siriushla.as_ma_control import SiriusMagnetControlWindow
from siriushla.as_config_manager import ConfigManagerWindow

class ControlApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self._windows = list()
        self._setupUi()

    def _setupUi(self):
        openCyclePanel = QAction("PS Cycling", self)
        openCyclePanel.triggered.connect(self._openCyclePanel)

        openLTBMagnetControlPanel = QAction("LTB Magnets", self)
        openLTBMagnetControlPanel.triggered.connect(self._openLTBMagnetsWindow)
        openBoosterMagnetControlPanel = QAction("Booster Magnets", self)
        openBoosterMagnetControlPanel.triggered.connect(self._openBoosterMagnetsWindow)
        openBTSMagnetControlPanel = QAction("BTS Magnets", self)
        openBTSMagnetControlPanel.triggered.connect(self._openBTSMagnetsWindow)
        openSiriusMagnetControlPanel = QAction("Sirius Magnets", self)
        openSiriusMagnetControlPanel.triggered.connect(self._openSiriusMagnetsWindow)

        openBoosterConfiguration = QAction("Booster Configuration", self)
        openBoosterConfiguration.triggered.connect(lambda: self._openConfigurationWindow('BoForcePvs'))
        openSiriusConfiguration = QAction("Sirius Configuration", self)
        openSiriusConfiguration.triggered.connect(lambda: self._openConfigurationWindow('SiForcePvs'))

        menubar = QMenuBar(self)
        menubar.setNativeMenuBar(False)

        psMenu = menubar.addMenu("Power Supplies")
        psMenu.addAction(openCyclePanel)

        magnetsMenu = menubar.addMenu("&Magnet")
        magnetsMenu.addAction(openLTBMagnetControlPanel)
        magnetsMenu.addAction(openBoosterMagnetControlPanel)
        magnetsMenu.addAction(openBTSMagnetControlPanel)
        magnetsMenu.addAction(openSiriusMagnetControlPanel)

        configMenu = menubar.addMenu("&Configuration Control")
        configMenu.addAction(openBoosterConfiguration)
        configMenu.addAction(openSiriusConfiguration)

        self.setMenuBar(menubar)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Test Application")
        self.show()

    def _openCyclePanel(self, section):
        self._windows.append(PsCycleWindow(self))
        self._windows[-1].open()

    def _openConfigurationWindow(self, section):
        self._windows.append(ConfigManagerWindow(section, self))
        self._windows[-1].show()

    @pyqtSlot()
    def _openSiriusMagnetsWindow(self):
        self._windows.append(SiriusMagnetControlWindow(self))
        self._windows[-1].open()

    @pyqtSlot()
    def _openBTSMagnetsWindow(self):
        self._windows.append(ToSiriusMagnetControlWindow(self))
        self._windows[-1].open()

    @pyqtSlot()
    def _openBoosterMagnetsWindow(self):
        self._windows.append(BoosterMagnetControlWindow(self))
        self._windows[-1].open()

    @pyqtSlot()
    def _openLTBMagnetsWindow(self):
        self._windows.append(ToBoosterMagnetControlWindow(self))
        self._windows[-1].open()


if __name__ == "__main__":
    app = PyDMApplication(None, sys.argv)
    window = ControlApplication()
    sys.exit(app.exec_())
