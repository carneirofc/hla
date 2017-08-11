import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QSpacerItem as QSpIt
from PyQt5.QtWidgets import QSizePolicy as QSzPol
from pydm import PyDMApplication
from pydm.widgets.checkbox import PyDMCheckbox as PyDMCb
from pydm.widgets.enum_combo_box import PyDMEnumComboBox as PyDMECB
from pydm.widgets.led import PyDMLed
from pydm.widgets.label import PyDMLabel
from pydm.widgets.spinbox import PyDMSpinBox
from pydm.widgets.pushbutton import PyDMPushButton
from siriuspy.envars import vaca_prefix as PREFIX
from siriuspy.namesys import SiriusPVName as _PVName

PREFIX = 'fac' + PREFIX[8:]


class _BaseCntrler(QGroupBox):
    """Template for control of High Level Triggers."""

    _MIN_WIDs = {}
    _LABELS = {}
    _ALL_PROPS = tuple()

    def __init__(self, parent=None, prefix='', hl_props=set(), header=False):
        """Initialize object."""
        super().__init__(parent)
        self.prefix = _PVName(prefix)
        self.hl_props = hl_props
        self.header = header
        self.setupUi()

    def setupUi(self):
        self.lh = QHBoxLayout(self)
        self.setLayout(self.lh)
        self.setContentsMargins(0, 0, 0, 0)
        self.lh.addItem(QSpIt(5, 20, QSzPol.Expanding, QSzPol.Minimum))
        for prop in self._ALL_PROPS:
            self.addColumn(prop)

    def addColumn(self, prop):
        if prop not in self.hl_props:
            return
        if not self.header:
            lv = QVBoxLayout()
            objs = self._createObjs(prop)
            for ob in objs:
                lv.addWidget(ob)
                ob.setMinimumWidth(self._MIN_WIDs[prop])
            self.lh.addItem(lv)
        else:
            self.lh.addWidget(self._headerLabel(prop))
        self.lh.addItem(QSpIt(5, 20, QSzPol.Expanding, QSzPol.Minimum))

    def _headerLabel(self, prop):
        lb = QLabel(self._LABELS[prop], self)
        lb.setAlignment(Qt.AlignHCenter)
        lb.setMinimumWidth(self._MIN_WIDs[prop])
        return lb

    def _createObjs(self, prop):
        return tuple()  # return tuple of objects


class EventCntrler(_BaseCntrler):
    """Template for control of Events."""

    _MIN_WIDs = {'ext_trig': 70, 'mode': 120, 'delay_type': 70, 'delay': 100}
    _LABELS = {'ext_trig': 'Ext. Trig.', 'mode': 'Mode',
               'delay_type': 'Delay Type', 'delay': 'Delay [us]'}
    _ALL_PROPS = ('ext_trig', 'mode', 'delay_type', 'delay')

    def _createObjs(self, prop):
        pv_pref = 'ca://' + PREFIX + self.prefix
        if 'ext_trig' == prop:
            sp = PyDMPushButton(self, init_channel=pv_pref+'ExtTrig-Cmd',
                                pressValue=1)
            sp.setText(self.prefix.propty)
            return (sp, )
        elif 'mode' == prop:
            sp = PyDMECB(self, init_channel=pv_pref + "Mode-Sel")
            rb = PyDMLabel(self, init_channel=pv_pref + "Mode-Sts")
        elif 'delay_type' == prop:
            sp = PyDMECB(self, init_channel=pv_pref+"DelayType-Sel")
            rb = PyDMLabel(self, init_channel=pv_pref+"DelayType-Sts")
        elif 'duration' == prop:
            sp = PyDMSpinBox(self, init_channel=pv_pref + "Delay-SP",
                             step=1e-3, limits_from_pv=True)
            rb = PyDMLabel(self, init_channel=pv_pref + "Delay-RB",
                           prec_from_pv=True)
        elif 'polarity' == prop:
            sp = PyDMECB(self, init_channel=pv_pref + "Polrty-Sel")
            rb = PyDMLabel(self, init_channel=pv_pref+"Polrty-Sts")
        elif 'delay' == prop:
            sp = PyDMSpinBox(self, init_channel=pv_pref + "Delay-SP",
                             step=1e-4, limits_from_pv=True)
            rb = PyDMLabel(self, init_channel=pv_pref + "Delay-RB",
                           prec_from_pv=True)
        return sp, rb


class HLTrigCntrler(_BaseCntrler):
    """Template for control of High Level Triggers."""

    _MIN_WIDs = {'state': 200, 'evg_param': 100, 'pulses': 70, 'duration': 150,
                 'polarity': 70, 'delay': 150}
    _LABELS = {'state': 'State', 'evg_param': 'EVG Params',
               'pulses': 'Nr Pulses', 'duration': 'Train Duration [ms]',
               'polarity': 'Polarity', 'delay': 'Delay [us]'}
    _ALL_PROPS = ('state', 'evg_param', 'pulses', 'duration', 'polarity',
                  'delay')

    def _createObjs(self, prop):
        pv_pref = 'ca://' + PREFIX + self.prefix
        if 'state' == prop:
            sp = PyDMCb(self, init_channel=pv_pref + "State-Sel")
            sp.setText(self.prefix)
            rb = PyDMLed(self, init_channel=pv_pref + "State-Sts")
        elif 'evg_param' == prop:
            sp = PyDMECB(self, init_channel=pv_pref + "EVGParam-Sel")
            rb = PyDMLabel(self, init_channel=pv_pref+"EVGParam-Sts")
        elif 'pulses' == prop:
            sp = PyDMSpinBox(self, init_channel=pv_pref + "Pulses-SP",
                             step=1, limits_from_pv=True, precision=0)
            rb = PyDMLabel(self, init_channel=pv_pref + "Pulses-RB",
                           prec_from_pv=True)
        elif 'duration' == prop:
            sp = PyDMSpinBox(self, init_channel=pv_pref + "Duration-SP",
                             step=1e-4, limits_from_pv=True)
            rb = PyDMLabel(self, init_channel=pv_pref + "Duration-RB",
                           prec_from_pv=True)
        elif 'polarity' == prop:
            sp = PyDMECB(self, init_channel=pv_pref + "Polrty-Sel")
            rb = PyDMLabel(self, init_channel=pv_pref+"Polrty-Sts")
        elif 'delay' == prop:
            sp = PyDMSpinBox(self, init_channel=pv_pref + "Delay-SP",
                             step=1e-4, limits_from_pv=True)
            rb = PyDMLabel(self, init_channel=pv_pref + "Delay-RB",
                           prec_from_pv=True)
        return sp, rb


def main():
    """Run Example."""
    app = PyDMApplication()
    ev_ctrl = EventCntrler(prefix='AS-Glob:TI-EVG:Linac')
    ev_ctrl.show()
    hl_props = {'evg_param', 'state', 'pulses', 'duration'}
    cl_ctrl = HLTrigCntrler(prefix='SI-Glob:TI-Corrs:', hl_props=hl_props)
    cl_ctrl.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
