"""LI Egun control."""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QGridLayout, QLabel, QGroupBox, \
    QSpacerItem, QSizePolicy as QSzPlcy
import qtawesome as qta

from pydm.widgets import PyDMLabel

from siriuspy.envars import VACA_PREFIX

from siriushla.widgets import SiriusMainWindow, SiriusLedState, \
    SiriusSpinbox, PyDMStateButton
from siriushla.util import get_appropriate_color


class LIEgunWindow(SiriusMainWindow):
    """Linac Egun Control Window."""

    def __init__(self, parent=None, prefix=VACA_PREFIX):
        """Init."""
        super().__init__(parent)
        self.prefix = prefix
        self.setWindowTitle('Linac E-gun Control Window')
        color = get_appropriate_color('LI')
        self.setWindowIcon(qta.icon('mdi.spotlight-beam', color=color))
        self.setObjectName('LIApp')
        self._setupUi()

    def _setupUi(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)

        self.title = QLabel('<h2>Linac E-gun</h2>', self)

        wid_sysstatus = self._setupSysStatusWidget()
        wid_hvps = self._setupHVPSWidget()
        wid_trigger = self._setupTriggerWidget()
        wid_filaps = self._setupFilaPSWidget()
        wid_biasps = self._setupBiasPSWidget()
        wid_pulseps = self._setupPulsePSWidget()
        wid_multipulseps = self._setupMultiPulsePSWidget()

        layout = QGridLayout(cw)
        layout.setVerticalSpacing(12)
        layout.setHorizontalSpacing(12)
        layout.addWidget(self.title, 0, 0, 1, 6)
        layout.addWidget(wid_sysstatus, 1, 0, 1, 1)
        layout.addWidget(wid_hvps, 1, 1, 1, 4)
        layout.addWidget(wid_trigger, 1, 5)
        layout.addWidget(wid_filaps, 2, 0, 1, 6)
        layout.addWidget(wid_biasps, 3, 0, 1, 6)
        layout.addWidget(wid_pulseps, 4, 0, 1, 3)
        layout.addWidget(wid_multipulseps, 4, 3, 1, 3)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 2)
        layout.setColumnStretch(4, 2)
        layout.setColumnStretch(5, 3)

        self.setStyleSheet("""
            QLabel{
                qproperty-alignment: AlignCenter;
            }""")

    def _setupSysStatusWidget(self):
        self._ld_sysvalve = QLabel('Valve', self)
        self._led_sysvalve = SiriusLedState(
            self, self.prefix+'LI-01:EG-Valve:status')

        self._ld_sysgate = QLabel('Gate', self)
        self._led_sysgate = SiriusLedState(
            self, self.prefix+'LI-01:EG-Gate:status')

        self._ld_sysvac = QLabel('Vacuum', self)
        self._led_sysvac = SiriusLedState(
            self, self.prefix+'LI-01:EG-Vacuum:status')

        self._ld_sysplc = QLabel('PLC', self)
        self._led_sysplc = SiriusLedState(
            self, self.prefix+'LI-01:EG-PLC:status')
        self._led_sysplc.offColor = SiriusLedState.Yellow

        self._ld_syssysstart = QLabel('System\nStart', self)
        self._bt_syssysstart = PyDMStateButton(
            self, self.prefix+'LI-01:EG-System:start')

        wid = QGroupBox('System Status', self)
        lay = QGridLayout(wid)
        lay.addWidget(self._ld_sysvalve, 0, 0)
        lay.addWidget(self._led_sysvalve, 0, 1)
        lay.addWidget(self._ld_sysgate, 1, 0)
        lay.addWidget(self._led_sysgate, 1, 1)
        lay.addWidget(self._ld_sysvac, 2, 0)
        lay.addWidget(self._led_sysvac, 2, 1)
        lay.addWidget(self._ld_sysplc, 3, 0)
        lay.addWidget(self._led_sysplc, 3, 1)
        lay.addWidget(self._ld_syssysstart, 4, 0)
        lay.addWidget(self._bt_syssysstart, 4, 1)
        return wid

    def _setupHVPSWidget(self):
        self._ld_hvpsswtsel = QLabel('Switch', self)
        self._bt_hvpsswtsel = PyDMStateButton(
            self, self.prefix+'LI-01:EG-HVPS:switch')

        self._ld_hvpsswtsts = QLabel('Status', self)
        self._led_hvpsswtsts = SiriusLedState(
            self, self.prefix+'LI-01:EG-HVPS:swstatus')

        self._ld_hvpsvoltsp = QLabel('Voltage SP [kV]', self)
        self._sb_hvpsvoltsp = SiriusSpinbox(
            self, self.prefix+'LI-01:EG-HVPS:voltoutsoft')
        self._sb_hvpsvoltsp.showStepExponent = False

        self._ld_hvpsvoltrb = QLabel('Voltage RB [kV]', self)
        self._lb_hvpsvoltrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-HVPS:voltinsoft')

        self._ld_hvpsenblsel = QLabel('Enable')
        self._bt_hvpsenblsel = PyDMStateButton(
            self, self.prefix+'LI-01:EG-HVPS:enable')

        self._ld_hvpsenblsts = QLabel('Status')
        self._led_hvpsenblsts = SiriusLedState(
            self, self.prefix+'LI-01:EG-HVPS:enstatus')

        self._ld_hvpscurrsp = QLabel('Current SP [mA]')
        self._sb_hvpscurrsp = SiriusSpinbox(
            self, self.prefix+'LI-01:EG-HVPS:currentoutsoft')
        self._sb_hvpscurrsp.showStepExponent = False

        self._ld_hvpscurrrb = QLabel('Current RB [mA]')
        self._lb_hvpscurrrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-HVPS:currentinsoft')

        wid = QGroupBox('High Voltage Power Supply', self)
        lay = QGridLayout(wid)
        lay.addWidget(self._ld_hvpsswtsel, 0, 0)
        lay.addWidget(self._bt_hvpsswtsel, 1, 0)
        lay.addWidget(self._ld_hvpsswtsts, 0, 1)
        lay.addWidget(self._led_hvpsswtsts, 1, 1)
        lay.addWidget(self._ld_hvpsvoltsp, 0, 2)
        lay.addWidget(self._sb_hvpsvoltsp, 1, 2)
        lay.addWidget(self._ld_hvpsvoltrb, 0, 3)
        lay.addWidget(self._lb_hvpsvoltrb, 1, 3)
        lay.addItem(QSpacerItem(1, 15, QSzPlcy.Ignored, QSzPlcy.Fixed), 2, 0)
        lay.addWidget(self._ld_hvpsenblsel, 3, 0)
        lay.addWidget(self._bt_hvpsenblsel, 4, 0)
        lay.addWidget(self._ld_hvpsenblsts, 3, 1)
        lay.addWidget(self._led_hvpsenblsts, 4, 1)
        lay.addWidget(self._ld_hvpscurrsp, 3, 2)
        lay.addWidget(self._sb_hvpscurrsp, 4, 2)
        lay.addWidget(self._ld_hvpscurrrb, 3, 3)
        lay.addWidget(self._lb_hvpscurrrb, 4, 3)
        return wid

    def _setupTriggerWidget(self):
        self._ld_trigsts = QLabel('Status', self)
        self._led_trigsts = SiriusLedState(
            self, self.prefix+'LI-01:EG-TriggerPS:status')

        self._ld_trigall = QLabel('Trigger Allow', self)
        self._led_trigall = SiriusLedState(
            self, self.prefix+'LI-01:EG-TriggerPS:allow')

        self._ld_trigenbl = QLabel('Trigger', self)
        self._bt_trigenblsel = PyDMStateButton(
            self, self.prefix+'LI-01:EG-TriggerPS:enable')
        self._led_trigenblsts = SiriusLedState(
            self, self.prefix+'LI-01:EG-TriggerPS:enablereal')

        wid = QGroupBox('Trigger', self)
        lay = QGridLayout(wid)
        lay.addWidget(self._ld_trigsts, 0, 0, 1, 2)
        lay.addWidget(self._led_trigsts, 1, 0, 1, 2)
        lay.addWidget(self._ld_trigall, 2, 0, 1, 2)
        lay.addWidget(self._led_trigall, 3, 0, 1, 2)
        lay.addWidget(self._ld_trigenbl, 4, 0, 1, 2)
        lay.addWidget(self._bt_trigenblsel, 5, 0)
        lay.addWidget(self._led_trigenblsts, 5, 1)
        return wid

    def _setupFilaPSWidget(self):
        self._ld_filaswtsel = QLabel('Switch', self)
        self._bt_filaswtsel = PyDMStateButton(
            self, self.prefix+'LI-01:EG-FilaPS:switch')

        self._ld_filaswtsts = QLabel('Status', self)
        self._led_filasswtsts = SiriusLedState(
            self, self.prefix+'LI-01:EG-FilaPS:swstatus')

        self._ld_filacurrsp = QLabel('Current SP [A]', self)
        self._sb_filacurrsp = SiriusSpinbox(
            self, self.prefix+'LI-01:EG-FilaPS:currentoutsoft')
        self._sb_filacurrsp.showStepExponent = False

        self._ld_filacurrrb = QLabel('Current RB [A]', self)
        self._lb_filacurrrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-FilaPS:currentinsoft')

        self._ld_filavoltrb = QLabel('Voltage RB [V]', self)
        self._lb_filavoltrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-FilaPS:voltinsoft')

        wid = QGroupBox('Filament Power Supply', self)
        lay = QGridLayout(wid)
        lay.addWidget(self._ld_filaswtsel, 0, 0)
        lay.addWidget(self._bt_filaswtsel, 1, 0)
        lay.addWidget(self._ld_filaswtsts, 0, 1)
        lay.addWidget(self._led_filasswtsts, 1, 1)
        lay.addWidget(self._ld_filacurrsp, 0, 2)
        lay.addWidget(self._sb_filacurrsp, 1, 2)
        lay.addWidget(self._ld_filacurrrb, 0, 3)
        lay.addWidget(self._lb_filacurrrb, 1, 3)
        lay.addWidget(self._ld_filavoltrb, 0, 4)
        lay.addWidget(self._lb_filavoltrb, 1, 4)
        return wid

    def _setupBiasPSWidget(self):
        self._ld_biasswtsel = QLabel('Switch', self)
        self._bt_biasswtsel = PyDMStateButton(
            self, self.prefix+'LI-01:EG-BiasPS:switch')

        self._ld_biasswtsts = QLabel('Status', self)
        self._led_biassswtsts = SiriusLedState(
            self, self.prefix+'LI-01:EG-BiasPS:swstatus')

        self._ld_biasvoltsp = QLabel('Voltage SP [V]', self)
        self._sb_biasvoltsp = SiriusSpinbox(
            self, self.prefix+'LI-01:EG-BiasPS:voltoutsoft')
        self._sb_biasvoltsp.showStepExponent = False

        self._ld_biasvoltrb = QLabel('Voltage RB [V]', self)
        self._lb_biasvoltrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-BiasPS:voltinsoft')

        self._ld_biascurrrb = QLabel('Current RB [A]', self)
        self._lb_biascurrrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-BiasPS:currentinsoft')

        wid = QGroupBox('Bias Power Supply', self)
        lay = QGridLayout(wid)
        lay.addWidget(self._ld_biasswtsel, 0, 0)
        lay.addWidget(self._bt_biasswtsel, 1, 0)
        lay.addWidget(self._ld_biasswtsts, 0, 1)
        lay.addWidget(self._led_biassswtsts, 1, 1)
        lay.addWidget(self._ld_biasvoltsp, 0, 2)
        lay.addWidget(self._sb_biasvoltsp, 1, 2)
        lay.addWidget(self._ld_biasvoltrb, 0, 3)
        lay.addWidget(self._lb_biasvoltrb, 1, 3)
        lay.addWidget(self._ld_biascurrrb, 0, 4)
        lay.addWidget(self._lb_biascurrrb, 1, 4)
        return wid

    def _setupPulsePSWidget(self):
        self._ld_pulsemodsel = QLabel('Mode', self)
        self._ld_pulsemodsts = QLabel('Status', self)
        self._ld_pulseswtsel = QLabel('Switch', self)
        self._ld_pulseswtsts = QLabel('Status', self)
        self._ld_pulsesing = QLabel('Single', self)
        self._ld_pulsemult = QLabel('Multi', self)

        self._bt_pulsesingmod = PyDMStateButton(
            self, self.prefix+'LI-01:EG-PulsePS:singleselect')
        self._led_pulsesingmod = SiriusLedState(
            self, self.prefix+'LI-01:EG-PulsePS:singleselstatus')
        self._bt_pulsesingswt = PyDMStateButton(
            self, self.prefix+'LI-01:EG-PulsePS:singleswitch')
        self._led_pulsesingswt = SiriusLedState(
            self, self.prefix+'LI-01:EG-PulsePS:singleswstatus')

        self._bt_pulsemultmod = PyDMStateButton(
            self, self.prefix+'LI-01:EG-PulsePS:multiselect')
        self._led_pulsemultmod = SiriusLedState(
            self, self.prefix+'LI-01:EG-PulsePS:multiselstatus')
        self._bt_pulsemultswt = PyDMStateButton(
            self, self.prefix+'LI-01:EG-PulsePS:multiswitch')
        self._led_pulsemultswt = SiriusLedState(
            self, self.prefix+'LI-01:EG-PulsePS:multiswstatus')

        wid = QGroupBox('Pulse Power Supply', self)
        lay = QGridLayout(wid)
        lay.addWidget(self._ld_pulsemodsel, 0, 1)
        lay.addWidget(self._ld_pulsemodsts, 0, 2)
        lay.addWidget(self._ld_pulseswtsel, 0, 3)
        lay.addWidget(self._ld_pulseswtsts, 0, 4)
        lay.addWidget(self._ld_pulsesing, 1, 0)
        lay.addWidget(self._ld_pulsemult, 2, 0)
        lay.addWidget(self._bt_pulsesingmod, 1, 1)
        lay.addWidget(self._led_pulsesingmod, 1, 2)
        lay.addWidget(self._bt_pulsesingswt, 1, 3)
        lay.addWidget(self._led_pulsesingswt, 1, 4)
        lay.addWidget(self._bt_pulsemultmod, 2, 1)
        lay.addWidget(self._led_pulsemultmod, 2, 2)
        lay.addWidget(self._bt_pulsemultswt, 2, 3)
        lay.addWidget(self._led_pulsemultswt, 2, 4)
        return wid

    def _setupMultiPulsePSWidget(self):
        self._ld_mpulspwrsp = QLabel('Power SP [V]', self)
        self._sb_mpulspwrsp = SiriusSpinbox(
            self, self.prefix+'LI-01:EG-PulsePS:poweroutsoft')
        self._sb_mpulspwrsp.limitsFromChannel = False
        self._sb_mpulspwrsp.setMinimum(0)
        self._sb_mpulspwrsp.setMaximum(300)
        self._sb_mpulspwrsp.showStepExponent = False
        self._ld_mpulspwrrb = QLabel('Power RB [V]', self)
        self._lb_mpulspwrrb = PyDMLabel(
            self, self.prefix+'LI-01:EG-PulsePS:powerinsoft')

        wid = QGroupBox('Multi Pulse Power Supply', self)
        lay = QGridLayout(wid)
        lay.setAlignment(Qt.AlignVCenter)
        lay.addWidget(self._ld_mpulspwrsp, 0, 0)
        lay.addWidget(self._sb_mpulspwrsp, 1, 0)
        lay.addWidget(self._ld_mpulspwrrb, 0, 1)
        lay.addWidget(self._lb_mpulspwrrb, 1, 1)
        return wid
