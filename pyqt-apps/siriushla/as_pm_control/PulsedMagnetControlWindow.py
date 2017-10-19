"""Modulet that defines the window class that control pulsed mangets."""
from pydm import PyDMApplication
from pydm.PyQt.QtGui import QMainWindow, QWidget, QVBoxLayout, QTabWidget

from siriuspy.search import MASearch
from siriushla.as_ma_control.MagnetWidget import PulsedMagnetWidget
from siriushla.as_pm_control.PulsedMagnetDetailWindow \
    import PulsedMagnetDetailWindow
from ..util import connect_window


class PulsedMagnetControlWindow(QMainWindow):
    """Window to control pulsed magnets."""

    StyleSheet = """
    """

    def __init__(self, parent=None):
        """Constructor."""
        self.app = PyDMApplication.instance()

        super().__init__(parent)
        self._setup_ui()
        self.setStyleSheet(PulsedMagnetControlWindow.StyleSheet)

        # self.setAttribute(Qt.WA_DeleteOnClose)
        # self.app.establish_widget_connections(self)

    def _setup_ui(self):
        self.main_widget = QTabWidget(self)
        self.main_widget.layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_widget.layout)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("Pulsed magnets control window")
        self.setFocus()

        self.main_widget.addTab(self._make_tab_widget("TB"), "TB")
        self.main_widget.addTab(self._make_tab_widget("BO"), "Booster")
        self.main_widget.addTab(self._make_tab_widget("TS"), "TS")
        self.main_widget.addTab(self._make_tab_widget("SI"), "Storage Ring")

        self._connect_buttons()

    def _make_tab_widget(self, section):
        widget = QWidget(self)
        widget.layout = QVBoxLayout()

        magnets = MASearch.get_manames(
            {"section": section, "discipline": "PM"})

        header = True
        for magnet in magnets:
            ma_widget = PulsedMagnetWidget(magnet, header, self)
            widget.layout.addWidget(ma_widget)
            header &= False

        widget.layout.addStretch()

        widget.setLayout(widget.layout)
        return widget

    def _connect_buttons(self):
        """Return buttons in the PulsedMagnetWidgets."""
        widgets = self.main_widget.findChildren(PulsedMagnetWidget)
        for widget in widgets:
            maname = widget.maname
            button = widget.get_detail_button()
            connect_window(button, PulsedMagnetDetailWindow,
                           parent=self, maname=maname)
            # self._window_manager.register_window(
            #     maname + "_detail", PulsedMagnetDetailWindow,
            #     maname=maname, parent=self)
            # button.clicked.connect(lambda: self._window_manager.open_window(
            #     self.sender().text() + "_detail"))

    def showEvent(self, event):
        """Establish connections and call super."""
        self.app.establish_widget_connections(self)
        super().showEvent(event)

    def closeEvent(self, event):
        """Override closeEvent in order to close iwdget connections."""
        self.app.close_widget_connections(self)
        super().closeEvent(event)


if __name__ == "__main__":
    import sys

    app = PyDMApplication(None, sys.argv)
    w = PulsedMagnetControlWindow()
    w.show()
    sys.exit(app.exec_())
