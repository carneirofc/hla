import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QLabel, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QSizePolicy as QSzPol
from pydm.widgets.label import PyDMLabel
from siriuspy.namesys import SiriusPVName as _PVName
from siriushla.sirius_application import SiriusApplication
from siriushla.widgets.led import PyDMLed, SiriusLedAlert
from siriushla.widgets.state_button import PyDMStateButton
from siriushla.widgets.windows import SiriusMainWindow
from siriushla import util as _util


class FOUT(SiriusMainWindow):
    """Template for control of High Level Triggers."""

    def __init__(self, parent=None, prefix=''):
        """Initialize object."""
        super().__init__(parent)
        self.prefix = _PVName(prefix)
        self._setupUi()

    def _setupUi(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)
        self.my_layout = QGridLayout(cw)
        self.my_layout.setHorizontalSpacing(70)
        self.my_layout.setVerticalSpacing(40)
        lab = QLabel('<h1>' + self.prefix.device_name + '</h1>', cw)
        self.my_layout.addWidget(lab, 0, 0)
        self.my_layout.setAlignment(lab, Qt.AlignCenter)

        self.status_wid = QGroupBox('Status', self)
        self.my_layout.addWidget(self.status_wid, 1, 0)
        self._setup_status_wid()

    def _setup_status_wid(self):
        prefix = self.prefix
        status_layout = QGridLayout(self.status_wid)
        status_layout.setHorizontalSpacing(30)
        status_layout.setVerticalSpacing(30)

        sp = PyDMStateButton(self, init_channel=prefix + "DevEnbl-Sel")
        rb = PyDMLed(self, init_channel=prefix + "DevEnbl-Sts")
        rb.setMinimumHeight(40)
        rb.setSizePolicy(QSzPol.Preferred, QSzPol.Minimum)
        gb = self._create_small_GB(
            'Enabled', self.status_wid, (sp, rb), align_ver=False
            )
        status_layout.addWidget(gb, 0, 0)

        lb = QLabel("<b>Alive</b>")
        rb = PyDMLabel(self, init_channel=prefix + "Alive-Mon")
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 1)

        lb = QLabel("<b>Network</b>")
        rb = SiriusLedAlert(self, init_channel=prefix + "Network-Mon")
        on_c, off_c = rb.onColor, rb.offColor
        rb.offColor = on_c
        rb.onColor = off_c
        rb.setMaximumSize(40, 40)
        rb.setSizePolicy(QSzPol.Maximum, QSzPol.Maximum)
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 2)

        lb = QLabel("<b>UP Link</b>")
        rb = SiriusLedAlert(self, init_channel=prefix + "Link-Mon")
        on_c, off_c = rb.onColor, rb.offColor
        rb.offColor = on_c
        rb.onColor = off_c
        rb.setMaximumSize(40, 40)
        rb.setSizePolicy(QSzPol.Maximum, QSzPol.Maximum)
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 3)

        wids = list()
        for i in range(8):
            rb = SiriusLedAlert(
                self, init_channel=prefix + "Los-Mon", bit=i
                )
            rb.setMaximumSize(40, 40)
            rb.setSizePolicy(QSzPol.Maximum, QSzPol.Maximum)
            wids.append(rb)
        gb = self._create_small_GB(
                'Down Connection', self.status_wid, wids, align_ver=False
                )
        status_layout.addWidget(gb, 1, 0, 1, 4)

    def _create_small_GB(self, name, parent, wids, align_ver=True):
        gb = QGroupBox(name, parent)
        lv = QVBoxLayout(gb) if align_ver else QHBoxLayout(gb)
        for wid in wids:
            lv.addWidget(wid)
            lv.setAlignment(wid, Qt.AlignCenter)
        return gb


if __name__ == '__main__':
    """Run Example."""
    app = SiriusApplication()
    _util.set_style(app)
    fout_ctrl = FOUT(
        prefix='ca://fernando-lnls452-linux-AS-Glob:TI-FOUT-1:')
    fout_ctrl.show()
    sys.exit(app.exec_())