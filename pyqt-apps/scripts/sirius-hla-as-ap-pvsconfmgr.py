#!/usr/bin/env python-sirius

"""Lauch PVs configuration manager."""
import sys

import siriuspy.envars as _envars
from siriuspy.servconf.conf_service import ConfigService

from qtpy.QtWidgets import QWidget, QPushButton, QHBoxLayout

from siriushla.sirius_application import SiriusApplication
from siriushla.widgets.windows import SiriusMainWindow
from siriushla.util import connect_window
from siriushla.as_ap_pvsconfmgr import \
    SetConfigurationWindow, ReadConfigurationWindow


class PVConfiguration(SiriusMainWindow):
    """Window to manage configuration."""

    def __init__(self, parent=None):
        """Setup UI."""
        super().__init__(parent)
        self._db = ConfigService(_envars.server_url_configdb)
        self._setup_ui()
        self.setWindowTitle("PVs Configuration")

    def _setup_ui(self):
        self.central_widget = QWidget(self)
        self.central_widget.layout = QHBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.central_widget.layout)
        self.setCentralWidget(self.central_widget)

        self.save_btn = QPushButton('Save configuration', self)
        self.load_btn = QPushButton('Load configuration', self)
        self.save_btn.setObjectName('SaveBtn')
        self.load_btn.setObjectName('LoadBtn')

        self.central_widget.layout.addWidget(self.save_btn)
        self.central_widget.layout.addWidget(self.load_btn)

        self.central_widget.setStyleSheet("""
        #SaveBtn, #LoadBtn {
            background: qlineargradient(x1:0 y1:0, x2:0 y2:1,
                                        stop:0 white, stop:1 lightgrey);
            height: 100%;
            border: 1px solid grey;
            padding: 0 5px 0 5px;
        }
        #SaveBtn:hover, #LoadBtn:hover {
            background: qlineargradient(x1:0 y1:0, x2:0 y2:1,
                                        stop:0 lightgrey, stop:1 white);
        }""")

        connect_window(self.save_btn, ReadConfigurationWindow, self,
                       db=self._db)
        connect_window(self.load_btn, SetConfigurationWindow, self,
                       db=self._db)


if __name__ == '__main__':
    app = SiriusApplication()
    w = PVConfiguration()
    w.show()
    sys.exit(app.exec_())
