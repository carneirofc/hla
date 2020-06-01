"""Kyma APU Control module."""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel, \
    QHBoxLayout, QSizePolicy as QSzPlcy, QSpacerItem, QPushButton
import qtawesome as qta
from pydm.widgets import PyDMLabel, PyDMEnumComboBox, PyDMPushButton, \
    PyDMSpinbox

from siriuspy.envars import VACA_PREFIX as _vaca_prefix
from siriushla.util import connect_window
from siriushla.widgets import SiriusMainWindow, PyDMLed, SiriusLedAlert, \
    SiriusLedState, PyDMLedMultiChannel, PyDMStateButton
from .auxiliary_dialogs import APUAlarmDetails, APUInterlockDetails


class APUControlWindow(SiriusMainWindow):
    """Kyma APU Control Window."""

    def __init__(self, parent=None, prefix=_vaca_prefix, device=''):
        """Init."""
        super().__init__(parent)
        self._prefix = prefix
        self._device = device
        self.dev_pref = prefix + device
        self.setWindowTitle(device+' Control Window')
        self.setObjectName('SIApp')
        self._setupUi()

    def _setupUi(self):
        self._label_title = QLabel(
            '<h3>'+self._device+' Control</h3>', self,
            alignment=Qt.AlignCenter)

        cw = QWidget()
        lay = QGridLayout(cw)
        lay.addWidget(self._label_title, 0, 0, 1, 4)
        lay.addWidget(self._mainControlsWidget(), 1, 0, 2, 1)
        lay.addWidget(self._alarmAndInterlockWidget(), 1, 1, 2, 1)
        lay.addWidget(self._ctrlModeWidget(), 1, 2)
        lay.addWidget(self._beamLinesCtrlWidget(), 2, 2)
        lay.addWidget(self._auxCommandsWidget(), 3, 0)
        lay.addWidget(self._harwareAndLLWidget(), 3, 1, 1, 2)
        lay.setRowStretch(0, 1)
        lay.setRowStretch(1, 2)
        lay.setRowStretch(2, 2)
        lay.setRowStretch(2, 5)
        self.setCentralWidget(cw)

    def _mainControlsWidget(self):
        self._ld_phs = QLabel('Phase [mm]', self)
        self._sb_phs = PyDMSpinbox(self, self.dev_pref+':Phase-SP')
        self._sb_phs.showStepExponent = False
        self._lb_phs = PyDMLabel(self, self.dev_pref+':Phase-Mon')

        self._ld_phsspd = QLabel('Phase Speed\n[mm/s]', self)
        self._sb_phsspd = PyDMSpinbox(self, self.dev_pref+':PhaseSpeed-SP')
        self._sb_phsspd.showStepExponent = False
        self._lb_phsspd = PyDMLabel(self, self.dev_pref+':PhaseSpeed-Mon')

        self._ld_ismov = QLabel('Motion', self)
        self._led_ismov = SiriusLedState(self, self.dev_pref+':Moving-Mon')
        self._pb_start = PyDMPushButton(
            self, label='', icon=qta.icon('fa5s.play'))
        self._pb_start.setToolTip(
            'Start automatic motion towards previously entered setpoint.')
        self._pb_start.channel = self.dev_pref+':DevCtrl-Cmd'  # Start
        self._pb_start.pressValue = 3
        self._pb_start.setObjectName('Start')
        self._pb_start.setStyleSheet(
            '#Start{min-width:30px; max-width:30px; icon-size:25px;}')
        self._pb_stop = PyDMPushButton(
            self, label='', icon=qta.icon('fa5s.stop'))
        self._pb_stop.setToolTip('Stop all motion, lock all brakes.')
        self._pb_stop.channel = self.dev_pref+':DevCtrl-Cmd'  # Stop
        self._pb_stop.pressValue = 1
        self._pb_stop.setObjectName('Stop')
        self._pb_stop.setStyleSheet(
            '#Stop{min-width:30px; max-width:30px; icon-size:25px;}')
        hbox_motion = QHBoxLayout()
        hbox_motion.addWidget(self._pb_start)
        hbox_motion.addWidget(self._pb_stop)
        hbox_motion.addWidget(self._led_ismov)

        gbox_main = QGroupBox('Main Controls', self)
        lay_main = QGridLayout(gbox_main)
        lay_main.addWidget(self._ld_phs, 0, 0)
        lay_main.addWidget(self._sb_phs, 0, 1)
        lay_main.addWidget(self._lb_phs, 0, 2)
        lay_main.addWidget(self._ld_phsspd, 1, 0)
        lay_main.addWidget(self._sb_phsspd, 1, 1)
        lay_main.addWidget(self._lb_phsspd, 1, 2)
        lay_main.addItem(
            QSpacerItem(1, 10, QSzPlcy.Ignored, QSzPlcy.Fixed), 3, 0)
        lay_main.addWidget(self._ld_ismov, 4, 0)
        lay_main.addLayout(hbox_motion, 4, 1, 1, 2)
        return gbox_main

    def _alarmAndInterlockWidget(self):
        self._ld_alarm = QLabel(
            'Alarms', self, alignment=Qt.AlignCenter)
        self._led_alarm = SiriusLedAlert(self, self.dev_pref+':Alarm-Mon')
        self._pb_alarmdetail = QPushButton(
            qta.icon('fa5s.ellipsis-h'), '', self)
        self._pb_alarmdetail.setObjectName('dtl')
        self._pb_alarmdetail.setStyleSheet(
            "#dtl{min-width:25px; max-width:25px; icon-size:20px;}")
        connect_window(
            self._pb_alarmdetail, APUAlarmDetails, self,
            prefix=self._prefix, device=self._device)

        self._ld_intlk = QLabel(
            'Interlocks', self, alignment=Qt.AlignCenter)
        self._led_intlkresume = PyDMLedMultiChannel(
            self, {self.dev_pref+':IntlkInStop-Mon': 0,
                   self.dev_pref+':IntlkInEOpnGap-Mon': 0,
                   self.dev_pref+':IntlkOutStsOk-Mon': 1,
                   self.dev_pref+':IntlkOutCCPSEnbld-Mon': 1,
                   self.dev_pref+':IntlkOutPwrEnbld-Mon': 1})
        self._pb_intlkdetail = QPushButton(
            qta.icon('fa5s.ellipsis-h'), '', self)
        self._pb_intlkdetail.setObjectName('dtl')
        self._pb_intlkdetail.setStyleSheet(
            "#dtl{min-width:25px; max-width:25px; icon-size:20px;}")
        connect_window(
            self._pb_intlkdetail, APUInterlockDetails, self,
            prefix=self._prefix, device=self._device)

        self._ld_reset = QLabel(
            'Reset', self, alignment=Qt.AlignCenter)
        self._pb_reset = PyDMPushButton(
            self, label='', icon=qta.icon('fa5s.sync'))
        self._pb_reset.setToolTip('Reset active alarms.')
        self._pb_reset.channel = self.dev_pref+':DevCtrl-Cmd'  # Reset
        self._pb_reset.pressValue = 2
        self._pb_reset.setObjectName('Reset')
        self._pb_reset.setStyleSheet(
            '#Reset{min-width:30px; max-width:30px; icon-size:25px;}')

        gbox_alrmintlk = QGroupBox('Alarm&&Interlock')
        lay_alrmintlk = QGridLayout(gbox_alrmintlk)
        lay_alrmintlk.addWidget(self._pb_alarmdetail, 0, 0)
        lay_alrmintlk.addWidget(self._ld_alarm, 0, 1)
        lay_alrmintlk.addWidget(self._led_alarm, 0, 2)
        lay_alrmintlk.addWidget(self._pb_intlkdetail, 1, 0)
        lay_alrmintlk.addWidget(self._ld_intlk, 1, 1)
        lay_alrmintlk.addWidget(self._led_intlkresume, 1, 2)
        lay_alrmintlk.addWidget(self._ld_reset, 2, 1)
        lay_alrmintlk.addWidget(self._pb_reset, 2, 2)
        return gbox_alrmintlk

    def _ctrlModeWidget(self):
        self._led_ctrlmode = PyDMLed(self, self.dev_pref+':IsRemote-Mon')
        self._led_ctrlmode.offColor = PyDMLed.Red
        self._led_ctrlmode.onColor = PyDMLed.LightGreen
        self._lb_ctrlmode = PyDMLabel(self, self.dev_pref+':Interface-Mon')

        gbox_ctrlmode = QGroupBox('Control Mode')
        lay_ctrlmode = QHBoxLayout(gbox_ctrlmode)
        lay_ctrlmode.setAlignment(Qt.AlignCenter)
        lay_ctrlmode.addWidget(self._led_ctrlmode)
        lay_ctrlmode.addWidget(self._lb_ctrlmode)
        return gbox_ctrlmode

    def _beamLinesCtrlWidget(self):
        self._ld_blinesenbl = QLabel('Enable', self)
        self._sb_blinesenbl = PyDMStateButton(
            self, self.dev_pref+':BeamLineCtrlEnbl-Sel')
        self._led_blinesenbl = SiriusLedState(
            self, self.dev_pref+':BeamLineCtrlEnbl-Sts')
        self._ld_blinesmon = QLabel('Status', self)
        self._led_blinesmon = SiriusLedState(
            self, self.dev_pref+':BeamLineCtrl-Mon')

        gbox_blines = QGroupBox('Beam Lines Control', self)
        lay_blines = QGridLayout(gbox_blines)
        lay_blines.addWidget(self._ld_blinesenbl, 0, 0)
        lay_blines.addWidget(self._sb_blinesenbl, 0, 1)
        lay_blines.addWidget(self._led_blinesenbl, 0, 2)
        lay_blines.addWidget(self._ld_blinesmon, 1, 0)
        lay_blines.addWidget(self._led_blinesmon, 1, 1, 1, 2)
        return gbox_blines

    def _auxCommandsWidget(self):
        self._ld_speedlim = QLabel('Max Phase Speed\n[mm/s]', self)
        self._sb_speedlim = PyDMSpinbox(
            self, self.dev_pref+':PhaseSpeed-SP.DRVH')
        self._sb_speedlim.showStepExponent = False

        self._ld_homeaxis = QLabel('Do homing', self)
        self._pb_home = PyDMPushButton(
            self, label='', icon=qta.icon('mdi.keyboard-return'))
        self._pb_home.setToolTip('Execute homing for selected axis.')
        self._pb_home.channel = self.dev_pref+':DevCtrl-Cmd'  # Home
        self._pb_home.pressValue = 10
        self._pb_home.setObjectName('Home')
        self._pb_home.setStyleSheet(
            '#Home{min-width:30px; max-width:30px; icon-size:25px;}')
        self._cb_homeaxis = PyDMEnumComboBox(
            self, self.dev_pref+':HomeAxis-Sel')

        self._ld_calib = QLabel('Calibrate Tilt Meters', self)
        self._pb_calib = PyDMPushButton(
            self, label='', icon=qta.icon('fa5s.crosshairs'))
        self._pb_calib.setToolTip('Calibrate tilt meters.')
        self._pb_calib.channel = self.dev_pref+':DevCtrl-Cmd'  # CalibTilt
        self._pb_calib.pressValue = 4
        self._pb_calib.setObjectName('CalibTilt')
        self._pb_calib.setStyleSheet(
            '#CalibTilt{min-width:30px; max-width:30px; icon-size:25px;}')

        self._ld_standby = QLabel('Enable Standby Mode', self)
        self._pb_standby = PyDMPushButton(
            self, label='', icon=qta.icon('mdi.alpha-a-box-outline'))
        self._pb_standby.setToolTip(
            'Enable standby mode for automatic motion.')
        self._pb_standby.channel = self.dev_pref+':DevCtrl-Cmd'  # Standby
        self._pb_standby.pressValue = 5
        self._pb_standby.setObjectName('Standby')
        self._pb_standby.setStyleSheet(
            '#Standby{min-width:30px; max-width:30px; icon-size:25px;}')

        self._ld_lastcomm = QLabel('Last Command', self)
        self._lb_lastcomm = PyDMLabel(
            self, self.dev_pref+':LastDevCtrlCmd-Mon')

        gbox_auxcmd = QGroupBox('Auxiliary Commands', self)
        lay_auxcmd = QGridLayout(gbox_auxcmd)
        lay_auxcmd.addWidget(self._ld_speedlim, 0, 0)
        lay_auxcmd.addWidget(self._sb_speedlim, 0, 1, 1, 2)
        lay_auxcmd.addItem(
            QSpacerItem(1, 10, QSzPlcy.Ignored, QSzPlcy.Fixed), 1, 0)
        lay_auxcmd.addWidget(self._ld_homeaxis, 2, 0)
        lay_auxcmd.addWidget(self._cb_homeaxis, 2, 1)
        lay_auxcmd.addWidget(self._pb_home, 2, 2)
        lay_auxcmd.addWidget(self._ld_calib, 3, 0, 1, 2)
        lay_auxcmd.addWidget(self._pb_calib, 3, 2)
        lay_auxcmd.addWidget(self._ld_standby, 4, 0, 1, 2)
        lay_auxcmd.addWidget(self._pb_standby, 4, 2)
        lay_auxcmd.addWidget(self._ld_lastcomm, 5, 0)
        lay_auxcmd.addWidget(self._lb_lastcomm, 5, 1, 1, 2)
        lay_auxcmd.setColumnStretch(0, 4)
        lay_auxcmd.setColumnStretch(1, 2)
        lay_auxcmd.setColumnStretch(2, 1)
        return gbox_auxcmd

    def _harwareAndLLWidget(self):
        self._ld_stthw = QLabel('Hardware state', self)
        self._led_stthw = PyDMLedMultiChannel(
            self, channels2values={
                self.dev_pref+':StateHw-Mon':
                    {'value': [0x4C, 0x3C], 'comp': 'in'}})  # in [Op, Ready]
        self._led_stthw.offColor = PyDMLed.Yellow
        self._led_stthw.onColor = PyDMLed.LightGreen
        self._led_stthw.setStyleSheet('max-width: 1.29em;')
        self._led_stthw.setSizePolicy(QSzPlcy.Maximum, QSzPlcy.Preferred)
        self._lb_stthw = PyDMLabel(self, self.dev_pref+':StateHw-Mon')
        hbox_stthw = QHBoxLayout()
        hbox_stthw.addWidget(self._led_stthw)
        hbox_stthw.addWidget(self._lb_stthw)

        self._ld_sttsys = QLabel('System state', self)
        self._led_sttsys = PyDMLedMultiChannel(
            self, channels2values={self.dev_pref+':State-Mon': 1})  # 1: Op
        self._led_sttsys.offColor = PyDMLed.Yellow
        self._led_sttsys.onColor = PyDMLed.LightGreen
        self._led_sttsys.setStyleSheet('max-width: 1.29em;')
        self._led_sttsys.setSizePolicy(QSzPlcy.Maximum, QSzPlcy.Preferred)
        self._lb_sttsys = PyDMLabel(self, self.dev_pref+':State-Mon')
        hbox_sttsys = QHBoxLayout()
        hbox_sttsys.addWidget(self._led_sttsys)
        hbox_sttsys.addWidget(self._lb_sttsys)

        self._ld_isopr = QLabel('Is operational', self)
        self._led_isopr = PyDMLed(self, self.dev_pref+':IsOperational-Mon')
        self._led_isopr.offColor = PyDMLed.Red
        self._led_isopr.onColor = PyDMLed.LightGreen

        self._ld_motenbl = QLabel('Motors Enabled', self)
        self._led_motenbl = PyDMLed(self, self.dev_pref+':MotorsEnbld-Mon')
        self._led_motenbl.offColor = PyDMLed.Red
        self._led_motenbl.onColor = PyDMLed.LightGreen

        gbox_hwsys = QGroupBox('Hardware&&LowLevel')
        lay_hwsys = QGridLayout(gbox_hwsys)
        lay_hwsys.addWidget(self._ld_stthw, 2, 0)
        lay_hwsys.addLayout(hbox_stthw, 2, 1)
        lay_hwsys.addWidget(self._ld_sttsys, 3, 0)
        lay_hwsys.addLayout(hbox_sttsys, 3, 1)
        lay_hwsys.addWidget(self._ld_isopr, 4, 0)
        lay_hwsys.addWidget(self._led_isopr, 4, 1)
        lay_hwsys.addWidget(self._ld_motenbl, 5, 0)
        lay_hwsys.addWidget(self._led_motenbl, 5, 1)
        return gbox_hwsys
