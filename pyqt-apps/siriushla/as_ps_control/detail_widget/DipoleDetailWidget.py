"""Widget for controlling a dipole."""
import re

from pydm.PyQt.QtCore import Qt
from pydm.PyQt.QtGui import QGridLayout, QLabel, QSizePolicy, \
    QFrame, QHBoxLayout, QPushButton, QVBoxLayout

from siriuspy.envars import vaca_prefix
from pydm.widgets import PyDMLabel, PyDMEnumComboBox, PyDMSpinbox, PyDMLineEdit
from siriushla.widgets import SiriusMainWindow
from siriushla.widgets.state_button import PyDMStateButton
from siriushla.as_ps_control.detail_widget.PSDetailWidget \
    import PSDetailWidget
from siriushla.widgets import PyDMLinEditScrollbar
from siriushla.widgets.led import SiriusLedState, SiriusLedAlert
from siriushla import util as _util
from .MagnetInterlockWidget import MagnetInterlockWindow


class DipoleDetailWidget(PSDetailWidget):
    """Widget that allows controlling a dipole magnet."""

    def __init__(self, magnet_name, parent=None):
        """Class constructor."""
        self._vaca_prefix = vaca_prefix
        if re.match("(SI|BO)-Fam:MA-B\w*", magnet_name):
            self._magnet_name = magnet_name
            self._prefixed_magnet = self._vaca_prefix + self._magnet_name
        else:
            raise ValueError("Magnet not supported by this class!")

        ps_name = re.sub(":MA", ":PS", self._prefixed_magnet)
        self._ps_list = [ps_name + "-1",
                         ps_name + "-2"]

        super(DipoleDetailWidget, self).__init__(self._magnet_name, parent)

    def _interlockLayout(self):
        layout = QGridLayout()
        soft_intlk_button = QPushButton('Soft Interlock', self)
        hard_intlk_button = QPushButton('Hard Interlock', self)
        layout.addWidget(soft_intlk_button, 0, 0, 1, 2)
        layout.addWidget(SiriusLedAlert(
            self, "ca://" + self._ps_list[0] + ":IntlkSoft-Mon"), 1, 0)
        layout.addWidget(SiriusLedAlert(
            self, "ca://" + self._ps_list[1] + ":IntlkSoft-Mon"), 1, 1)
        layout.addWidget(hard_intlk_button, 2, 0, 1, 2)
        layout.addWidget(SiriusLedAlert(
            self, "ca://" + self._ps_list[0] + ":IntlkHard-Mon"), 3, 0)
        layout.addWidget(SiriusLedAlert(
            self, "ca://" + self._ps_list[1] + ":IntlkHard-Mon"), 3, 1)
        # Connect buttons to open magnet interlock windows
        _util.connect_window(soft_intlk_button, MagnetInterlockWindow, self,
                             **{'magnet': self._magnet_name,
                                'interlock': 0})
        _util.connect_window(hard_intlk_button, MagnetInterlockWindow, self,
                             **{'magnet': self._magnet_name,
                                'interlock': 1})
        return layout

    def _opModeLayout(self):
        layout = QGridLayout()

        self.opmode_sp = PyDMEnumComboBox(
            self, init_channel="ca://" + self._prefixed_magnet + ":OpMode-Sel")
        self.opmode1_rb = PyDMLabel(
            self, "ca://" + self._ps_list[0] + ":OpMode-Sts")
        self.opmode1_rb.setObjectName("opmode1_rb_label")
        self.ctrlmode1_led = SiriusLedAlert(
            self, "ca://" + self._ps_list[0] + ":CtrlMode-Mon")
        self.ctrlmode1_label = PyDMLabel(
            self, "ca://" + self._ps_list[0] + ":CtrlMode-Mon")
        self.ctrlmode1_label.setObjectName("ctrlmode1_label")
        self.opmode2_rb = PyDMLabel(
            self, "ca://" + self._ps_list[1] + ":OpMode-Sts")
        self.opmode2_rb.setObjectName("opmode2_rb_label")
        self.ctrlmode2_led = SiriusLedAlert(
            self, "ca://" + self._ps_list[1] + ":CtrlMode-Mon")
        self.ctrlmode2_label = PyDMLabel(
            self, "ca://" + self._ps_list[1] + ":CtrlMode-Mon")
        self.ctrlmode2_label.setObjectName("ctrlmode2_label")

        self.ctrlmode1_led.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.ctrlmode2_led.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)

        ps1_layout = QGridLayout()
        # ps1_layout.addWidget(QLabel("PS1"), 0, 0, 1, 2)
        # ps1_layout.addWidget(self.opmode1_rb, 0, 0, 1, 2)
        ps1_layout.addWidget(self.ctrlmode1_led, 1, 0)
        ps1_layout.addWidget(self.ctrlmode1_label, 1, 1)

        ps2_layout = QGridLayout()
        # ps2_layout.addWidget(QLabel("PS2"), 0, 0, 1, 2)
        # ps2_layout.addWidget(self.opmode2_rb, 0, 0, 1, 2)
        ps2_layout.addWidget(self.ctrlmode2_led, 1, 0)
        ps2_layout.addWidget(self.ctrlmode2_label, 1, 1)

        layout.addWidget(self.opmode_sp, 0, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.opmode1_rb, 1, 0)
        layout.addWidget(self.opmode2_rb, 1, 1)
        layout.addLayout(ps1_layout, 2, 0)
        layout.addLayout(ps2_layout, 2, 1)
        # layout.setColumnStretch(2, 1)

        return layout

    def _powerStateLayout(self):
        layout = QGridLayout()

        # self.on_btn = PyDMPushButton(
        #     self, label="On", pressValue=1,
        #     init_channel="ca://" + self._prefixed_magnet + ":PwrState-Sel")
        # self.off_btn = PyDMPushButton(
        #     self, label="Off", pressValue=0,
        #     init_channel="ca://" + self._prefixed_magnet + ":PwrState-Sel")

        self.state_button = PyDMStateButton(
            parent=self,
            init_channel="ca://" + self._prefixed_magnet + ":PwrState-Sel")

        self.pwrstate1_led = SiriusLedState(
            self, "ca://" + self._ps_list[0] + ":PwrState-Sts")
        self.pwrstate1_label = PyDMLabel(
            self, "ca://" + self._ps_list[0] + ":PwrState-Sts")
        self.pwrstate1_label.setObjectName("pwrstate1_label")
        self.pwrstate2_led = SiriusLedState(
            self, "ca://" + self._ps_list[1] + ":PwrState-Sts")
        self.pwrstate2_label = PyDMLabel(
            self, "ca://" + self._ps_list[1] + ":PwrState-Sts")
        self.pwrstate2_label.setObjectName("pwrstate2_label")

        self.state_button.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.pwrstate1_led.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.pwrstate2_led.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)

        # buttons_layout = QHBoxLayout()
        # buttons_layout.addWidget(self.on_btn)
        # buttons_layout.addWidget(self.off_btn)
        pwrstatus_layout1 = QHBoxLayout()
        pwrstatus_layout2 = QHBoxLayout()
        # pwrstatus_layout.addWidget(QLabel("PS1"), 0, 0, 1, 2)
        # pwrstatus_layout.addWidget(QLabel("PS2"), 0, 2, 1, 2)
        pwrstatus_layout1.addWidget(self.pwrstate1_led)
        pwrstatus_layout1.addWidget(self.pwrstate1_label)
        pwrstatus_layout2.addWidget(self.pwrstate2_led)
        pwrstatus_layout2.addWidget(self.pwrstate2_label)

        layout.addWidget(self.state_button, 0, 0, 1, 2)
        layout.addLayout(pwrstatus_layout1, 1, 0, Qt.AlignCenter)
        layout.addLayout(pwrstatus_layout2, 1, 1, Qt.AlignCenter)
        # layout.addStretch(1)

        return layout

    def _currentLayout(self):
        layout = QGridLayout()

        self.current_sp_label = QLabel("Setpoint")
        self.current_rb_label = QLabel("Readback")
        self.current_ref_label = QLabel("Ref Mon")
        self.current_mon_label = QLabel("Mon")

        self.current_sp_widget = PyDMLinEditScrollbar(
            parent=self,
            channel="ca://" + self._prefixed_magnet + ":Current-SP")
        # self.current_sp_widget.set_limits_from_pv(True)
        self.current_sp_widget.sp_scrollbar.setTracking(False)
        # Current RB
        self.current_rb_val = PyDMLabel(
            self, "ca://" + self._prefixed_magnet + ":Current-RB")
        self.current_rb_val.precFromPV = True
        self.ps1_current_rb = PyDMLabel(
            self, "ca://" + self._ps_list[0] + ":Current-RB")
        self.ps1_current_rb.precFromPV = True
        self.ps2_current_rb = PyDMLabel(
            self, "ca://" + self._ps_list[1] + ":Current-RB")
        self.ps2_current_rb.precFromPV = True
        # Current Ref
        self.current_ref_val = PyDMLabel(
            self, "ca://" + self._prefixed_magnet + ":CurrentRef-Mon")
        self.current_ref_val.precFromPV = True
        self.ps1_current_ref = PyDMLabel(
            self, "ca://" + self._ps_list[0] + ":CurrentRef-Mon")
        self.ps1_current_ref.precFromPV = True
        self.ps2_current_ref = PyDMLabel(
            self, "ca://" + self._ps_list[1] + ":CurrentRef-Mon")
        self.ps2_current_ref.precFromPV = True
        # Current Mon
        self.current_mon_val = PyDMLabel(
            self, "ca://" + self._prefixed_magnet + ":Current-Mon")
        self.current_mon_val.precFromPV = True
        self.ps1_current_mon = PyDMLabel(
            self, "ca://" + self._ps_list[0] + ":Current-Mon")
        self.ps1_current_mon.precFromPV = True
        self.ps2_current_mon = PyDMLabel(
            self, "ca://" + self._ps_list[1] + ":Current-Mon")
        self.ps2_current_mon.precFromPV = True

        # Horizontal rulers
        hr1 = QFrame(self)
        hr1.setFrameShape(QFrame.HLine)
        hr1.setFrameShadow(QFrame.Sunken)
        hr2 = QFrame(self)
        hr2.setFrameShape(QFrame.HLine)
        hr2.setFrameShadow(QFrame.Sunken)
        hr3 = QFrame(self)
        hr3.setFrameShape(QFrame.HLine)
        hr3.setFrameShadow(QFrame.Sunken)

        layout.addWidget(self.current_sp_label, 0, 0, Qt.AlignRight)
        layout.addWidget(self.current_sp_widget, 0, 1, 1, 2)
        layout.addWidget(hr3, 1, 0, 1, 3)
        layout.addWidget(self.current_rb_label, 2, 0, Qt.AlignRight)
        layout.addWidget(self.current_rb_val, 2, 1)
        # layout.addWidget(QLabel("PS1"), 1, 2)
        layout.addWidget(self.ps1_current_rb, 2, 2)
        # layout.addWidget(QLabel("PS2"), 2, 2)
        layout.addWidget(self.ps2_current_rb, 3, 2)
        layout.addWidget(hr1, 4, 0, 1, 3)
        layout.addWidget(self.current_ref_label, 5, 0, Qt.AlignRight)
        layout.addWidget(self.current_ref_val, 5, 1)
        # layout.addWidget(QLabel("PS1"), 3, 2)
        layout.addWidget(self.ps1_current_ref, 5, 2)
        # layout.addWidget(QLabel("PS2"), 4, 2)
        layout.addWidget(self.ps2_current_ref, 6, 2)
        layout.addWidget(hr2, 7, 0, 1, 3)
        layout.addWidget(self.current_mon_label, 8, 0, Qt.AlignRight)
        layout.addWidget(self.current_mon_val, 8, 1)
        # layout.addWidget(QLabel("PS1"), 5, 2)
        layout.addWidget(self.ps1_current_mon, 8, 2)
        # layout.addWidget(QLabel("PS2"), 6, 2)
        layout.addWidget(self.ps2_current_mon, 9, 2)
        # layout.addWidget(self.current_sp_slider, 3, 1)
        # layout.setRowStretch(10, 1)
        layout.setColumnStretch(3, 1)

        return layout

    def _cycleLayout(self):
        layout = QGridLayout()
        # 15 cycle pvs
        enbl_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleEnbl-SP'
        enbl_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleEnbl-RB'
        enbl_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleEnbl-RB'
        type_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleType-Sel'
        type_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleType-Sts'
        type_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleType-Sts'
        nrcycles_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleNrCycles-SP'
        nrcycles_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleNrCycles-RB'
        nrcycles_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleNrCycles-RB'
        index_ca1 = 'ca://' + self._ps_list[0] + ':CycleIndex-Mon'
        index_ca2 = 'ca://' + self._ps_list[1] + ':CycleIndex-Mon'
        freq_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleFreq-SP'
        freq_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleFreq-RB'
        freq_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleFreq-RB'
        ampl_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleAmpl-SP'
        ampl_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleAmpl-RB'
        ampl_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleAmpl-RB'
        offset_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleOffset-SP'
        offset_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleOffset-RB'
        offset_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleOffset-RB'
        auxparam_sp_ca = 'ca://' + self._prefixed_magnet + ':CycleAuxParam-SP'
        auxparam_rb_ca1 = 'ca://' + self._ps_list[0] + ':CycleAuxParam-RB'
        auxparam_rb_ca2 = 'ca://' + self._ps_list[1] + ':CycleAuxParam-RB'
        # 8 labels
        self.cycle_enbl_label = QLabel('Enabled', self)
        self.cycle_type_label = QLabel('Type', self)
        self.cycle_nr_label = QLabel('Nr. Cycles', self)
        self.cycle_index_label = QLabel('Index', self)
        self.cycle_freq_label = QLabel('Frequency', self)
        self.cycle_ampl_label = QLabel('Amplitude', self)
        self.cycle_offset_label = QLabel('Offset', self)
        self.cycle_auxparam_label = QLabel('AuxParams', self)
        # 15 widgets
        self.cycle_enbl_sp_button = PyDMStateButton(self, enbl_sp_ca)
        self.cycle_enbl_rb_led1 = SiriusLedState(self, enbl_rb_ca1)
        self.cycle_enbl_rb_led2 = SiriusLedState(self, enbl_rb_ca2)
        enbl_rb_layout = QVBoxLayout()
        enbl_rb_layout.addWidget(self.cycle_enbl_rb_led1)
        enbl_rb_layout.addWidget(self.cycle_enbl_rb_led2)
        self.cycle_type_sp_cb = PyDMEnumComboBox(self, type_sp_ca)
        self.cycle_type_rb_label1 = PyDMLabel(self, type_rb_ca1)
        self.cycle_type_rb_label2 = PyDMLabel(self, type_rb_ca2)
        type_rb_layout = QVBoxLayout()
        type_rb_layout.addWidget(self.cycle_type_rb_label1)
        type_rb_layout.addWidget(self.cycle_type_rb_label2)
        self.cycle_nr_sp_sb = PyDMSpinbox(self, nrcycles_sp_ca)
        self.cycle_nr_rb_label1 = PyDMLabel(self, nrcycles_rb_ca1)
        self.cycle_nr_rb_label2 = PyDMLabel(self, nrcycles_rb_ca2)
        nrcycles_rb_layout = QVBoxLayout()
        nrcycles_rb_layout.addWidget(self.cycle_nr_rb_label1)
        nrcycles_rb_layout.addWidget(self.cycle_nr_rb_label2)
        self.cycle_index_mon_label1 = PyDMLabel(self, index_ca1)
        self.cycle_index_mon_label2 = PyDMLabel(self, index_ca2)
        index_mon_layout = QVBoxLayout()
        index_mon_layout.addWidget(self.cycle_index_mon_label1)
        index_mon_layout.addWidget(self.cycle_index_mon_label2)
        self.cycle_freq_sp_sb = PyDMSpinbox(self, freq_sp_ca)
        self.cycle_freq_rb_label1 = PyDMLabel(self, freq_rb_ca1)
        self.cycle_freq_rb_label2 = PyDMLabel(self, freq_rb_ca2)
        freq_rb_layout = QVBoxLayout()
        freq_rb_layout.addWidget(self.cycle_freq_rb_label1)
        freq_rb_layout.addWidget(self.cycle_freq_rb_label2)
        self.cycle_ampl_sp_sb = PyDMSpinbox(self, ampl_sp_ca)
        self.cycle_ampl_rb_label1 = PyDMLabel(self, ampl_rb_ca1)
        self.cycle_ampl_rb_label2 = PyDMLabel(self, ampl_rb_ca2)
        ampl_rb_layout = QVBoxLayout()
        ampl_rb_layout.addWidget(self.cycle_ampl_rb_label1)
        ampl_rb_layout.addWidget(self.cycle_ampl_rb_label2)
        self.cycle_offset_sp_sb = PyDMSpinbox(self, offset_sp_ca)
        self.cycle_offset_rb_label1 = PyDMLabel(self, offset_rb_ca1)
        self.cycle_offset_rb_label2 = PyDMLabel(self, offset_rb_ca2)
        offset_rb_layout = QVBoxLayout()
        offset_rb_layout.addWidget(self.cycle_offset_rb_label1)
        offset_rb_layout.addWidget(self.cycle_offset_rb_label2)
        self.cycle_auxparam_sp_le = PyDMLineEdit(self, auxparam_sp_ca)
        self.cycle_auxparam_rb_label1 = PyDMLabel(self, auxparam_rb_ca1)
        self.cycle_auxparam_rb_label2 = PyDMLabel(self, auxparam_rb_ca2)
        auxparam_rb_layout = QVBoxLayout()
        auxparam_rb_layout.addWidget(self.cycle_auxparam_rb_label1)
        auxparam_rb_layout.addWidget(self.cycle_auxparam_rb_label2)

        layout.addWidget(self.cycle_enbl_label, 0, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_enbl_sp_button, 0, 1)
        layout.addLayout(enbl_rb_layout, 0, 2)
        layout.addWidget(self.cycle_type_label, 1, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_type_sp_cb, 1, 1)
        layout.addLayout(type_rb_layout, 1, 2)
        layout.addWidget(self.cycle_nr_label, 2, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_nr_sp_sb, 2, 1)
        layout.addLayout(nrcycles_rb_layout, 2, 2)
        layout.addWidget(self.cycle_index_label, 3, 0, Qt.AlignRight)
        layout.addLayout(index_mon_layout, 3, 2)
        layout.addWidget(self.cycle_freq_label, 4, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_freq_sp_sb, 4, 1)
        layout.addLayout(freq_rb_layout, 4, 2)
        layout.addWidget(self.cycle_ampl_label, 5, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_ampl_sp_sb, 5, 1)
        layout.addLayout(ampl_rb_layout, 5, 2)
        layout.addWidget(self.cycle_offset_label, 6, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_offset_sp_sb, 6, 1)
        layout.addLayout(offset_rb_layout, 6, 2)
        layout.addWidget(self.cycle_auxparam_label, 7, 0, Qt.AlignRight)
        layout.addWidget(self.cycle_auxparam_sp_le, 7, 1)
        layout.addLayout(auxparam_rb_layout, 7, 2)

        return layout


if __name__ == "__main__":
    import sys
    from pydm import PyDMApplication
    app = PyDMApplication(None, [])

    w = SiriusMainWindow()
    w.setCentralWidget(DipoleDetailWidget("SI-Fam:MA-B1B2", w))
    w.setStyleSheet("""
    """)
    w.show()

    sys.exit(app.exec_())
