"""Defines a class to control elements from a given class."""
from pydm.PyQt.QtGui import QDialog, QTabWidget, QVBoxLayout, QApplication
from .MagnetDetailWindow import MagnetDetailWindow
from .MagnetTrimWindow import MagnetTrimWindow


class BaseMagnetControlWindow(QDialog):
    """Base window class to control elements of a given section."""

    DETAIL = 0
    TRIM = 1

    _window = None

    STYLESHEET = """
    * {font-size: 16px;}
    .QGroupBox {
        font-size: 20px;
        font-weight: bold;
    }
    .PyDMScrollBar {
        border: 1px solid black;
    }
    """

    def __init__(self, parent=None):
        """Class constructor."""
        super(BaseMagnetControlWindow, self).__init__(parent)
        self._setupUi()
        self.setStyleSheet(self.STYLESHEET)

        self.app = QApplication.instance()
        self.app.establish_widget_connections(self)

    def _setupUi(self):
        self.layout = QVBoxLayout()

        # Create Tabs
        self.tabs = QTabWidget()
        self._addTabs()

        # Set widget layout
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def _addTabs(self): pass

    def _connectButtons(self, buttons):
        for button in buttons:
            try:
                type_ = button.objectName().split("_")[0]
                if type_ in ["label", "trim"]:
                    button.clicked.connect(self._openWindow)
            except Exception:
                pass

    def _openWindow(self):
        sender = self.sender()

        name_split = sender.objectName().split("_")
        type_ = name_split[0]
        ma = name_split[1]

        if ma:
            if type_ == "label":
                self._window = MagnetDetailWindow(ma, self)
            elif type_ == "trim":
                self._window = MagnetTrimWindow(ma, self)

        self._window.exec_()

    def closeEvent(self, event):
        """Reimplement closed event to close widget connections."""
        self.app.close_widget_connections(self)
        super().closeEvent(event)
