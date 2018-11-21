#!/usr/bin/env python-sirius

"""Lauch PVs configuration manager."""
import sys

from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout

from siriushla import util as _util
from siriushla.sirius_application import SiriusApplication
from siriushla.widgets.windows import SiriusMainWindow
from siriushla.as_ap_pvsconfmgr import \
    SetConfigurationWindow, ReadConfigurationWindow
from siriuspy.servconf.conf_service import ConfigService


class PVConfiguration(SiriusMainWindow):
    """Window to manage configuration."""

    def __init__(self, parent=None):
        """Setup UI."""
        super().__init__(parent)
        self._setup_ui()
        self._db = ConfigService('http://10.0.7.55:8085')
        self._windows = []
        self.setWindowTitle("PVs Configuration")

    def _setup_ui(self):
        self.central_widget = QWidget(self)
        self.central_widget.layout = QHBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.central_widget.layout)
        self.setCentralWidget(self.central_widget)

        self.save_btn = QPushButton('Save new configuration', self)
        self.load_btn = QPushButton('Load new configuration', self)
        self.save_btn.setObjectName('SaveBtn')
        self.load_btn.setObjectName('LoadBtn')

        self.central_widget.layout.addWidget(self.save_btn)
        self.central_widget.layout.addWidget(self.load_btn)

        self.save_btn.clicked.connect(self._save_configuration)
        self.load_btn.clicked.connect(self._load_configuration)

    def _save_configuration(self):
        window = ReadConfigurationWindow(self._db, parent=self)
        self._windows.append(window)
        window.show()

    def _load_configuration(self):
        window = SetConfigurationWindow(self._db, parent=self)
        self._windows.append(window)
        window.show()


if __name__ == '__main__':
    app = SiriusApplication()
    _util.set_style(app)
    w = PVConfiguration()

    w.setStyleSheet("""
        #SaveBtn, #LoadBtn {
            background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 white, stop:1 lightgrey);
            height: 100%;
            font: 20pt;
            border: 1px solid grey;
            padding: 0 5px 0 5px;
        }
        #SaveBtn:hover, #LoadBtn:hover {
            background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 lightgrey, stop:1 white);
        }
    """)

    w.show()

    sys.exit(app.exec_())