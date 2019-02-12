import sys
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QGroupBox, QLabel, QPushButton, QFormLayout, \
    QVBoxLayout, QGridLayout, QSizePolicy as QSzPol, QWidget
from pydm.widgets import PyDMLabel
from siriuspy.search import HLTimeSearch
from siriuspy.csdevice import timesys
from siriushla.widgets import PyDMLed, SiriusLedAlert, PyDMStateButton
from siriushla.util import connect_window
from siriushla.widgets.windows import create_window_from_widget
from siriushla.as_ti_control.base import BaseList, BaseWidget, \
    MySpinBox as _MySpinBox, MyComboBox as _MyComboBox
from siriushla.as_ti_control.ll_trigger import \
    LLTriggerList, OTPList, OUTList, AFCOUTList


class HLTriggerDetailed(BaseWidget):
    """Template for control of High Level Triggers."""

    def __init__(self, parent=None, prefix=''):
        """Initialize object."""
        super().__init__(parent, prefix)
        self._setupUi()

    def _setupUi(self):
        self.my_layout = QGridLayout(self)
        self.my_layout.setHorizontalSpacing(20)
        self.my_layout.setVerticalSpacing(20)
        lab = QLabel('<h1>' + self.prefix.device_name + '</h1>', self)
        self.my_layout.addWidget(lab, 0, 0, 1, 2)
        self.my_layout.setAlignment(lab, Qt.AlignCenter)
        self.status_wid = QGroupBox('Status', self)
        self.my_layout.addWidget(self.status_wid, 1, 0)
        self._setup_status_wid()
        self.ll_list_wid = QGroupBox('Configs', self)
        self.my_layout.addWidget(self.ll_list_wid, 1, 1)
        self._setup_ll_list_wid()

    def _setup_status_wid(self):
        status_layout = QFormLayout(self.status_wid)
        status_layout.setHorizontalSpacing(20)
        status_layout.setVerticalSpacing(20)
        for bit, label in enumerate(timesys.Const.HLTrigStatusLabels):
            led = SiriusLedAlert(
                    self, self.prefix.substitute(propty='Status-Mon'), bit)
            lab = QLabel(label, self)
            status_layout.addRow(led, lab)

    def _setup_ll_list_wid(self):
        prefix = self.prefix
        ll_list_layout = QGridLayout(self.ll_list_wid)
        ll_list_layout.setHorizontalSpacing(20)
        ll_list_layout.setVerticalSpacing(20)

        but = QPushButton('Open LL Triggers', self)
        obj_names = HLTimeSearch.get_ll_trigger_names(self.prefix.device_name)
        Window = create_window_from_widget(LLTriggers, name='LLTriggers')
        connect_window(
            but, Window, self, prefix=self.prefix.prefix + '-',
            obj_names=obj_names)
        ll_list_layout.addWidget(but, 0, 0, 1, 2)

        init_channel = prefix.substitute(propty="State-Sel")
        sp = PyDMStateButton(self, init_channel=init_channel)
        init_channel = prefix.substitute(propty="State-Sts")
        rb = PyDMLed(self, init_channel=init_channel)
        gb = self._create_small_GB('Enabled', self.ll_list_wid, (sp, rb))
        ll_list_layout.addWidget(gb, 1, 0)

        init_channel = prefix.substitute(propty="Polarity-Sel")
        sp = _MyComboBox(self, init_channel=init_channel)
        init_channel = prefix.substitute(propty="Polarity-Sts")
        rb = PyDMLabel(self, init_channel=init_channel)
        gb = self._create_small_GB('Polarity', self.ll_list_wid, (sp, rb))
        ll_list_layout.addWidget(gb, 1, 1)

        init_channel = prefix.substitute(propty="Src-Sel")
        sp = _MyComboBox(self, init_channel=init_channel)
        init_channel = prefix.substitute(propty="Src-Sts")
        rb = PyDMLabel(self, init_channel=init_channel)
        gb = self._create_small_GB('Source', self.ll_list_wid, (sp, rb))
        ll_list_layout.addWidget(gb, 2, 0)

        init_channel = prefix.substitute(propty="NrPulses-SP")
        sp = _MySpinBox(self, init_channel=init_channel)
        sp.showStepExponent = False
        init_channel = prefix.substitute(propty="NrPulses-RB")
        rb = PyDMLabel(self, init_channel=init_channel)
        gb = self._create_small_GB('Nr Pulses', self.ll_list_wid, (sp, rb))
        ll_list_layout.addWidget(gb, 2, 1)

        init_channel = prefix.substitute(propty="Duration-SP")
        sp = _MySpinBox(self, init_channel=init_channel)
        sp.showStepExponent = False
        init_channel = prefix.substitute(propty="Duration-RB")
        rb = PyDMLabel(self, init_channel=init_channel)
        gb = self._create_small_GB('Duration [ms]', self.ll_list_wid, (sp, rb))
        ll_list_layout.addWidget(gb, 3, 0, 1, 2)

        init_channel = prefix.substitute(propty="Delay-SP")
        sp = _MySpinBox(self, init_channel=init_channel)
        sp.showStepExponent = False
        init_channel = prefix.substitute(propty="Delay-RB")
        rb = PyDMLabel(self, init_channel=init_channel)
        gb = self._create_small_GB('Delay [us]', self.ll_list_wid, (sp, rb))
        ll_list_layout.addWidget(gb, 4, 0, 1, 2)

        if HLTimeSearch.has_bypass_interlock(self.prefix.device_name):
            init_channel = prefix.substitute(propty="ByPassIntlk-Sel")
            sp = PyDMStateButton(self, init_channel=init_channel)
            sp.shape = 1
            sp.setSizePolicy(QSzPol.Minimum, QSzPol.Maximum)
            init_channel = prefix.substitute(propty="ByPassIntlk-Sts")
            rb = PyDMLed(self, init_channel=init_channel)
            rb.setSizePolicy(QSzPol.Minimum, QSzPol.Maximum)
            gb = self._create_small_GB(
                        'ByPass Intlk', self.ll_list_wid, (sp, rb))
            ll_list_layout.addWidget(gb, 5, 0)

        if HLTimeSearch.has_delay_type(self.prefix.device_name):
            init_channel = prefix.substitute(propty="RFDelayType-Sel")
            sp = _MyComboBox(self, init_channel=init_channel)
            init_channel = prefix.substitute(propty="RFDelayType-Sts")
            rb = PyDMLabel(self, init_channel=init_channel)
            gb = self._create_small_GB(
                        'Delay Type', self.ll_list_wid, (sp, rb))
            ll_list_layout.addWidget(gb, 5, 1)

    def _create_small_GB(self, name, parent, wids):
        gb = QGroupBox(name, parent)
        lv = QVBoxLayout(gb)
        for wid in wids:
            lv.addWidget(wid)
        return gb


class LLTriggers(QWidget):

    def __init__(self, parent=None, prefix=None, obj_names=list()):
        super().__init__(parent)
        vl = QVBoxLayout(self)
        vl.addWidget(QLabel('<h1>Low Level Triggers</h1>', self,
                            alignment=Qt.AlignCenter))

        amc_list = set()
        otp_list = set()
        out_list = set()
        for name in obj_names:
            if 'AMC' in name.dev:
                amc_list.add(name)
            elif 'OTP' in name.propty_name:
                otp_list.add(name)
            elif 'OUT' in name.propty_name:
                out_list.add(name)
        if amc_list:
            props = set(AFCOUTList()._ALL_PROPS)
            props.add('device')
            vl.addWidget(LLTriggerList(name='AMC', parent=self, props=props,
                                       prefix=prefix, obj_names=amc_list))
        if otp_list:
            props = set(OUTList()._ALL_PROPS)
            props.add('device')
            vl.addWidget(LLTriggerList(name='OTP', parent=self, props=props,
                                       prefix=prefix, obj_names=otp_list))
        if out_list:
            props = set(OTPList()._ALL_PROPS)
            for prop in OUTList()._ALL_PROPS:
                props.add(prop)
            props.add('device')
            vl.addWidget(LLTriggerList(name='OUT', parent=self, props=props,
                                       prefix=prefix, obj_names=out_list))


class HLTriggerList(BaseList):
    """Template for control of High Level Triggers."""

    _MIN_WIDs = {
        'detailed': 9,
        'status': 4.8,
        'state': 3.8,
        'interlock': 6.5,
        'source': 4.8,
        'pulses': 3.2,
        'duration': 6.1,
        'polarity': 4.8,
        'delay_type': 4.2,
        'delay': 5.5,
        }
    _LABELS = {
        'detailed': 'Detailed View',
        'status': 'Status',
        'state': 'Enabled',
        'interlock': 'ByPass Intlk',
        'source': 'Source',
        'pulses': 'Nr Pulses',
        'duration': 'Duration [ms]',
        'polarity': 'Polarity',
        'delay_type': 'Type',
        'delay': 'Delay [us]',
        }
    _ALL_PROPS = (
        'detailed', 'state', 'interlock', 'source', 'polarity', 'pulses',
        'duration', 'delay_type', 'delay', 'status',
        )

    def _createObjs(self, prefix, prop):
        sp = rb = None
        if prop == 'detailed':
            sp = QPushButton(prefix.device_name, self)
            Window = create_window_from_widget(
                HLTriggerDetailed, name='HLTriggerDetailed')
            connect_window(sp, Window, self, prefix=prefix)
        elif prop == 'status':
            init_channel = prefix.substitute(propty="Status-Mon")
            sp = SiriusLedAlert(self, init_channel=init_channel)
            sp.setShape(sp.ShapeMap.Square)
        elif prop == 'state':
            init_channel = prefix.substitute(propty="State-Sel")
            sp = PyDMStateButton(self, init_channel=init_channel)
            init_channel = prefix.substitute(propty="State-Sts")
            rb = PyDMLed(self, init_channel=init_channel)
        elif prop == 'interlock':
            init_channel = prefix.substitute(propty="ByPassIntlk-Sel")
            sp = PyDMStateButton(self, init_channel=init_channel)
            init_channel = prefix.substitute(propty="ByPassIntlk-Sts")
            rb = PyDMLed(self, init_channel=init_channel)
        elif prop == 'source':
            init_channel = prefix.substitute(propty="Src-Sel")
            sp = _MyComboBox(self, init_channel=init_channel)
            init_channel = prefix.substitute(propty="Src-Sts")
            rb = PyDMLabel(self, init_channel=init_channel)
        elif prop == 'pulses':
            init_channel = prefix.substitute(propty="NrPulses-SP")
            sp = _MySpinBox(self, init_channel=init_channel)
            sp.showStepExponent = False
            init_channel = prefix.substitute(propty="NrPulses-RB")
            rb = PyDMLabel(self, init_channel=init_channel)
        elif prop == 'duration':
            init_channel = prefix.substitute(propty="Duration-SP")
            sp = _MySpinBox(self, init_channel=init_channel)
            sp.showStepExponent = False
            init_channel = prefix.substitute(propty="Duration-RB")
            rb = PyDMLabel(self, init_channel=init_channel)
        elif prop == 'polarity':
            init_channel = prefix.substitute(propty="Polarity-Sel")
            sp = _MyComboBox(self, init_channel=init_channel)
            init_channel = prefix.substitute(propty="Polarity-Sts")
            rb = PyDMLabel(self, init_channel=init_channel)
        elif prop == 'delay_type':
            init_channel = prefix.substitute(propty="RFDelayType-Sel")
            sp = _MyComboBox(self, init_channel=init_channel)
            init_channel = prefix.substitute(propty="RFDelayType-Sts")
            rb = PyDMLabel(self, init_channel=init_channel)
        elif prop == 'delay':
            init_channel = prefix.substitute(propty="Delay-SP")
            sp = _MySpinBox(self, init_channel=init_channel)
            sp.showStepExponent = False
            init_channel = prefix.substitute(propty="Delay-RB")
            rb = PyDMLabel(self, init_channel=init_channel)
        else:
            raise Exception('Property unknown')
        if rb is None:
            return (sp, )
        return sp, rb


if __name__ == '__main__':
    """Run Example."""
    from siriushla.sirius_application import SiriusApplication
    from siriushla.widgets.windows import SiriusMainWindow

    props = {'detailed', 'state', 'pulses', 'duration'}
    app = SiriusApplication()
    win = SiriusMainWindow()
    list_ctrl = HLTriggerList(
        name="Triggers", props=props,
        obj_names=['BO-Fam:TI-Corrs-1', 'BO-Fam:TI-Corrs-2'])
    win.setCentralWidget(list_ctrl)
    win.show()
    sys.exit(app.exec_())
