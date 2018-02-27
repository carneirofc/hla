"""Defines a class to control a set of a device from a given class."""
from pydm import PyDMApplication

from siriushla.widgets import SiriusMainWindow
from .control_widget.ControlWidgetFactory import ControlWidgetFactory
from .MagnetDetailWindow import MagnetDetailWindow
from .MagnetTrimWindow import MagnetTrimWindow

from ..util import connect_window


class PSControlWindow(SiriusMainWindow):
    """Base window to show devices of a section in tabs."""

    def __init__(self, section, device, parent=None):
        """Class constructor."""
        super(PSControlWindow, self).__init__(parent)
        self.app = PyDMApplication.instance()
        self._section = section
        self._device = device

        self._setup_ui()

        # self.app.establish_widget_connections(self)

    def _setup_ui(self):
        # Set Widget
        self.widget = ControlWidgetFactory.factory(self._section, self._device)
        if self._device != "dipole":
            self._connect_buttons(self.widget)
        self.setCentralWidget(self.widget)

    def _connect_buttons(self, widget):
        # buttons = widget.get_detail_buttons()
        for widget in widget.get_magnet_widgets():
            maname = widget.maname
            detail_button = widget.get_detail_button()
            trim_button = widget.get_trim_button()

            connect_window(detail_button, MagnetDetailWindow,
                           self, maname=maname)

            if trim_button is not None:
                connect_window(trim_button, MagnetTrimWindow,
                               self, maname=maname)
