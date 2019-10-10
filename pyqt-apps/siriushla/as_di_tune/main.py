from qtpy.QtGui import QColor
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QGridLayout, QTabWidget, QVBoxLayout, \
    QLabel

from siriuspy.envars import vaca_prefix
from siriushla.widgets import SiriusMainWindow
from .spectrogram import BOTuneSpecControls
from .controls import BOTuneControls
from .details import BOTuneTrigger


class BOTune(SiriusMainWindow):
    """Booster Tune Window."""

    def __init__(self, parent=None, prefix=vaca_prefix):
        super().__init__(parent)
        self.prefix = prefix
        self.setObjectName('BOApp')
        self.setWindowTitle('Booster Tune')
        self._setupUi()
        self.setFocusPolicy(Qt.StrongFocus)

    def _setupUi(self):
        label = QLabel('<h2>Booster Tune<h2>', self,
                       alignment=Qt.AlignHCenter)
        label.setObjectName('label')
        label.setStyleSheet('#label{min-height: 1.29em; max-height: 1.29em;}')

        # Settings
        self.tabCtrl = QTabWidget(self)
        hcolor = QColor(179, 229, 255)
        vcolor = QColor(255, 179, 179)
        self.ctrlH = BOTuneControls(parent=self, prefix=self.prefix,
                                    orientation='H', background=hcolor)
        self.tabCtrl.addTab(self.ctrlH, 'Horizontal')
        self.ctrlV = BOTuneControls(parent=self, prefix=self.prefix,
                                    orientation='V', background=vcolor)
        self.tabCtrl.addTab(self.ctrlV, 'Vertical')
        self.tabCtrl.setStyleSheet("""
            QTabWidget::pane {
                border-left: 2px solid gray;
                border-bottom: 2px solid gray;
                border-right: 2px solid gray;
            }
            QTabBar::tab:first {
                background-color: #B3E5FF;
            }
            QTabBar::tab:last {
                background-color: #FFB3B3;
            }
            """)
        self.trig_gbox = BOTuneTrigger(self, self.prefix)
        vbox_sett = QVBoxLayout()
        vbox_sett.addWidget(self.tabCtrl)
        vbox_sett.addWidget(self.trig_gbox)

        # Sepctrograms
        self.specH = BOTuneSpecControls(
            parent=self, prefix=self.prefix, orientation='H',
            title='<h3>Horizontal</h3>', background=hcolor)
        self.specH.setObjectName('specH')

        self.specV = BOTuneSpecControls(
            parent=self, prefix=self.prefix, orientation='V',
            title='<h3>Vertical</h3>', background=vcolor)
        self.specV.setObjectName('specV')
        self.setStyleSheet(
            "#specH, #specV {min-width:32em; }")
        vbox_meas = QVBoxLayout()
        vbox_meas.addWidget(self.specH)
        vbox_meas.addSpacing(10)
        vbox_meas.addWidget(self.specV)

        cw = QWidget(self)
        lay = QGridLayout(cw)
        lay.addWidget(label, 0, 0, 1, 2)
        lay.addLayout(vbox_sett, 1, 0)
        lay.addLayout(vbox_meas, 1, 1)
        lay.setColumnStretch(0, 1)
        lay.setColumnStretch(1, 2)
        self.setCentralWidget(cw)