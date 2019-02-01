import sys
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel
from pydm.widgets.enum_combo_box import PyDMEnumComboBox as PyDMECB
from pydm.widgets.label import PyDMLabel
from pydm.widgets.spinbox import PyDMSpinbox
from siriuspy.search import LLTimeSearch
from siriushla.widgets.led import PyDMLed
from siriushla.widgets.state_button import PyDMStateButton
from siriushla.as_ti_control.base import BaseList


class LLTriggerList(BaseList):
    """Template for control of High Level Triggers."""

    _MIN_WIDs = {
        'name': 100,
        'device': 300,
        'state': 180,
        'event': 100,
        'width': 150,
        'polarity': 70,
        'pulses': 150,
        'delay': 150,
        'timestamp': 100,
        'interlock': 150,
        'source': 200,
        'trigger': 100,
        'rf_delay': 150,
        'fine_delay': 150,
        'rf_delay_type': 200,
        }
    _LABELS = {
        'name': 'Name',
        'device': 'Device',
        'state': 'State',
        'event': 'Event',
        'width': 'Width',
        'polarity': 'Polarity',
        'pulses': 'Nr Pulses',
        'delay': 'Delay',
        'timestamp': 'Log',
        'interlock': 'ByPassIntlk',
        'source': 'Source',
        'trigger': 'Trigger',
        'rf_delay': 'RF Delay',
        'fine_delay': 'Fine Delay',
        'rf_delay_type': 'RF Delay Type',
        }
    _ALL_PROPS = (
        'device', 'name', 'state', 'event', 'width', 'polarity', 'pulses',
        'delay', 'timestamp', 'interlock', 'source', 'trigger', 'rf_delay',
        'rf_delay_type', 'fine_delay')

    def _createObjs(self, prefix, prop):
        intlb = LLTimeSearch.get_channel_internal_trigger_pvname(prefix)
        outlb = LLTimeSearch.get_channel_output_port_pvname(prefix)
        sp = rb = None
        if prop == 'device':
            sp = QLabel(outlb.device_name, self)
            sp.setAlignment(Qt.AlignCenter)
        elif prop == 'name':
            sp = QLabel(outlb.propty, self)
            sp.setAlignment(Qt.AlignCenter)
        elif prop == 'state':
            pvname = intlb.substitute(propty=intlb.propty+"State-Sel")
            sp = PyDMStateButton(self, init_channel=pvname)
            pvname = intlb.substitute(propty=intlb.propty+"State-Sts")
            rb = PyDMLed(self, init_channel=pvname)
        elif prop == 'event':
            pvname = intlb.substitute(propty=intlb.propty+'Evt-SP')
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = intlb.substitute(propty=intlb.propty+'Evt-RB')
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'width':
            pvname = intlb.substitute(propty=intlb.propty+"Width-SP")
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = intlb.substitute(propty=intlb.propty+"Width-RB")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'polarity':
            pvname = intlb.substitute(propty=intlb.propty+"Polarity-Sel")
            sp = PyDMECB(self, init_channel=pvname)
            pvname = intlb.substitute(propty=intlb.propty+"Polarity-Sts")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'pulses':
            pvname = intlb.substitute(propty=intlb.propty+"NrPulses-SP")
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = intlb.substitute(propty=intlb.propty+"NrPulses-RB")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'delay':
            pvname = intlb.substitute(propty=intlb.propty+"Delay-SP")
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = intlb.substitute(propty=intlb.propty+"Delay-RB")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'timestamp':
            pvname = intlb.substitute(propty=intlb.propty+"Log-Sel")
            sp = PyDMStateButton(self, init_channel=pvname)
            pvname = intlb.substitute(propty=intlb.propty+"Log-Sts")
            rb = PyDMLed(self, init_channel=pvname)
        elif prop == 'interlock':
            pvname = intlb.substitute(propty=intlb.propty+"ByPassIntlk-Sel")
            sp = PyDMStateButton(self, init_channel=pvname)
            pvname = intlb.substitute(propty=intlb.propty+"ByPassIntlk-Sts")
            rb = PyDMLed(self, init_channel=pvname)
        if prop == 'source':
            pvname = outlb.substitute(propty=outlb.propty+"Src-Sel")
            sp = PyDMECB(self, init_channel=pvname)
            pvname = outlb.substitute(propty=outlb.propty+"Src-Sts")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'trigger':
            pvname = outlb.substitute(propty=outlb.propty+"SrcTrig-SP")
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = outlb.substitute(propty=outlb.propty+"SrcTrig-RB")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'rf_delay':
            pvname = outlb.substitute(propty=outlb.propty+"RFDelay-SP")
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = outlb.substitute(propty=outlb.propty+"RFDelay-RB")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'rf_delay_type':
            pvname = outlb.substitute(propty=outlb.propty+"RFDelayType-Sel")
            sp = PyDMECB(self, init_channel=pvname)
            pvname = outlb.substitute(propty=outlb.propty+"RFDelayType-Sts")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        elif prop == 'fine_delay':
            pvname = outlb.substitute(propty=outlb.propty+"FineDelay-SP")
            sp = PyDMSpinbox(self, init_channel=pvname)
            sp.showStepExponent = False
            pvname = outlb.substitute(propty=outlb.propty+"FineDelay-RB")
            rb = PyDMLabel(self, init_channel=pvname)
            rb.setAlignment(Qt.AlignCenter)
        if rb is None:
            return (sp, )
        return sp, rb


class OTPList(LLTriggerList):
    """Template for control of Timing devices Internal Triggers."""

    _ALL_PROPS = (
        'name', 'state', 'event', 'width', 'polarity', 'pulses', 'delay',
        'timestamp', 'interlock')


class OUTList(LLTriggerList):
    """Template for control of Timing Devices Output Channels."""

    _ALL_PROPS = (
        'name', 'source', 'trigger', 'rf_delay', 'rf_delay_type', 'fine_delay')


class AFCOUTList(LLTriggerList):
    """Template for control of Timing devices Internal Triggers."""

    _ALL_PROPS = (
        'name', 'state', 'event', 'source', 'width', 'polarity', 'pulses',
        'delay')


if __name__ == '__main__':
    """Run Example."""
    from siriushla.sirius_application import SiriusApplication
    app = SiriusApplication()
    props = {'device', 'name', 'state', 'pulses', 'width'}
    list_ctrl = LLTriggerList(
        name="Triggers", props=props,
        obj_names=['TEST-FAC:TI-EVR:OTP00', 'TEST-FAC:TI-EVE:OTP00'])
    list_ctrl.show()
    sys.exit(app.exec_())
