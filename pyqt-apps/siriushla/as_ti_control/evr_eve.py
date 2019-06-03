import sys
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QGroupBox, QLabel, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QSpacerItem, QSizePolicy as QSzPol
from pydm.widgets import PyDMLabel
from siriushla.widgets import PyDMLed, SiriusLedAlert, PyDMStateButton, \
    SiriusLedState
from siriushla.as_ti_control.base import BaseWidget, MyComboBox as _MyComboBox
from siriushla.as_ti_control.ll_trigger import OTPList, OUTList


class _EVR_EVE(BaseWidget):
    """Template for control of High Level Triggers."""

    def __init__(self, parent=None, prefix='', device='EVR'):
        """Initialize object."""
        super().__init__(parent, prefix)
        self.device_type = device
        self.setupui()

    def setupui(self):
        self.my_layout = QGridLayout(self)
        self.my_layout.setHorizontalSpacing(20)
        self.my_layout.setVerticalSpacing(20)
        lab = QLabel('<h1>' + self.prefix.device_name + '</h1>', self)
        self.my_layout.addWidget(lab, 0, 0, 1, 2)
        self.my_layout.setAlignment(lab, Qt.AlignCenter)

        self.otps_wid = OTPList(
            name='Internal Trigger (OTP)', parent=self, prefix=self.prefix,
            obj_names=['OTP{0:02d}'.format(i) for i in range(24)])
        self.otps_wid.setObjectName('otps_wid')
        self.otps_wid.setStyleSheet("""#otps_wid{min-width:60em;}""")
        self.my_layout.addWidget(self.otps_wid, 2, 0)

        self.outs_wid = OUTList(
            name='OUT', parent=self, prefix=self.prefix,
            obj_names=['OUT{0:d}'.format(i) for i in range(8)])
        self.outs_wid.setObjectName('outs_wid')
        self.outs_wid.setStyleSheet("""#outs_wid{min-width:44em;}""")
        self.my_layout.addWidget(self.outs_wid, 2, 1)
        self.my_layout.addItem(QSpacerItem(
                0, 0, QSzPol.Minimum, QSzPol.Expanding))

        self.status_wid = QGroupBox('Status', self)
        self.my_layout.addWidget(self.status_wid, 1, 0, 1, 2)
        self._setup_status_wid()

    def _setup_status_wid(self):
        prefix = self.prefix
        status_layout = QGridLayout(self.status_wid)
        status_layout.setHorizontalSpacing(30)
        status_layout.setVerticalSpacing(30)

        sp = PyDMStateButton(self, init_channel=prefix + "DevEnbl-Sel")
        rb = PyDMLed(self, init_channel=prefix + "DevEnbl-Sts")
        gb = self._create_small_GB(
            'Enabled', self.status_wid, (sp, rb), align_ver=False)
        status_layout.addWidget(gb, 0, 0)

        lb = QLabel("<b>Alive</b>")
        rb = PyDMLabel(self, init_channel=prefix + "Alive-Mon")
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 1)

        lb = QLabel("<b>Network</b>")
        rb = SiriusLedAlert(self, init_channel=prefix + "Network-Mon")
        rb.offColor, rb.onColor = rb.onColor, rb.offColor
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 2)

        lb = QLabel("<b>UP Link</b>")
        rb = SiriusLedAlert(self, init_channel=prefix + "LinkStatus-Mon")
        on_c, off_c = rb.onColor, rb.offColor
        rb.offColor = on_c
        rb.onColor = off_c
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 3)

        lb = QLabel("<b>Interlock Status</b>")
        rb = SiriusLedAlert(self, init_channel=prefix + "IntlkStatus-Mon")
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 4)

        lb = QLabel("<b>Interlock Enabled</b>")
        rb = SiriusLedState(self, init_channel=prefix + "IntlkEnbl-Mon")
        gb = self._create_small_GB('', self.status_wid, (lb, rb))
        gb.setStyleSheet('border: 2px solid transparent;')
        status_layout.addWidget(gb, 0, 5)

        if self.device_type == 'EVR':
            wids = list()
            for i in range(8):
                rb = SiriusLedAlert(
                    parent=self, init_channel=prefix + "Los-Mon", bit=i)
                wids.append(rb)
            gb = self._create_small_GB(
                    'Down Connection', self.status_wid, wids, align_ver=False)
        else:
            sp = _MyComboBox(self, init_channel=prefix + "RFOut-Sel")
            rb = PyDMLabel(self, init_channel=prefix + "RFOut-Sts")
            gb = self._create_small_GB('RF Output', self.status_wid, (sp, rb))
        status_layout.addWidget(gb, 0, 6)

    def _create_small_GB(self, name, parent, wids, align_ver=True):
        gb = QGroupBox(name, parent)
        lv = QVBoxLayout(gb) if align_ver else QHBoxLayout(gb)
        for wid in wids:
            lv.addWidget(wid)
            lv.setAlignment(wid, Qt.AlignCenter)
        return gb


class EVR(_EVR_EVE):

    def __init__(self, parent=None, prefix=''):
        super().__init__(parent, prefix, device='EVR')


class EVE(_EVR_EVE):

    def __init__(self, parent=None, prefix=''):
        super().__init__(parent, prefix, device='EVE')


if __name__ == '__main__':
    """Run Example."""
    from siriushla.sirius_application import SiriusApplication
    from siriushla.widgets.windows import SiriusMainWindow
    app = SiriusApplication()
    win = SiriusMainWindow()
    evr_ctrl = EVR(prefix='TEST-FAC:TI-EVR:')
    # eve_ctrl = EVE(prefix='TEST-FAC:TI-EVE:')
    win.setCentralWidget(evr_ctrl)
    # win.setCentralWidget(eve_ctrl)
    win.show()
    sys.exit(app.exec_())
