"""Defines a class to control a set of a device from a given class."""
import qtawesome as qta

from siriuspy.namesys import SiriusPVName as _PVName
from siriushla.util import connect_window, get_appropriate_color
from siriushla.widgets import SiriusMainWindow
from .control_widget.ControlWidgetFactory import ControlWidgetFactory
from .PSDetailWindow import PSDetailWindow
from .PSTrimWindow import PSTrimWindow


class PSControlWindow(SiriusMainWindow):
    """Base window to show devices of a section in tabs."""

    def __init__(self, section, device, subsection=None, parent=None):
        """Class constructor."""
        super(PSControlWindow, self).__init__(parent)
        self.setObjectName(section+'App')
        self._section = section
        self._device = device
        self._subsection = subsection
        icon = qta.icon(
            'mdi.car-battery', color=get_appropriate_color(section))
        self.setWindowIcon(icon)

        self._setup_ui()

        sec2label = {
            'TB': 'LTB ',
            'BO': 'Booster ',
            'TS': 'BTS ',
            'SI': 'Storage Ring '}
        dev2label = {
            'dipole': 'Dipoles ',
            'quadrupole': 'Quadrupoles ',
            'sextupole': 'Sextupoles ',
            'skew-quadrupole': 'Skew Quadrupoles ',
            'trim-quadrupole': 'Trims ',
            'corrector-slow': 'Slow Correctors '}
        #     'corrector-fast': 'Fast Correctors '}
        self.setWindowTitle(
            sec2label[section] +
            (dev2label[device] if device else '') +
            'Power Supplies ' +
            ('- Subsection '+subsection if subsection else ''))

    def _setup_ui(self):
        self.widget = ControlWidgetFactory.factory(
            parent=self, section=self._section,
            subsection=self._subsection, device=self._device)
        self._connect_buttons(self.widget)
        self.setCentralWidget(self.widget)

    def _connect_buttons(self, widget):
        for w in widget.get_summary_widgets():
            detail_bt = w.get_detail_button()
            psname = detail_bt.text()
            if not psname:
                psname = detail_bt.toolTip()
            psname = _PVName(psname)
            connect_window(detail_bt, PSDetailWindow, self, psname=psname)

            trim_bt = w.get_trim_button()
            if trim_bt is not None:
                connect_window(trim_bt, PSTrimWindow, self, device=psname)
