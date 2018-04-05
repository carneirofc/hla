"""Control of EVG Timing Device."""

import sys as _sys
import os as _os
from PyQt5 import uic as _uic
from PyQt5.QtWidgets import QVBoxLayout as _QVBoxLayout
from PyQt5.QtWidgets import QSizePolicy as _QSzPol
from PyQt5.QtWidgets import QSpacerItem as _QSpIt
from pydm import PyDMApplication as _PyDMApplication
from siriuspy.envars import vaca_prefix as PREFIX
from siriuspy.timesys.time_data import Clocks as _Clocks
from siriuspy.timesys.time_data import Events as _Events
from .list_widgets import EventList as _EventList
from .list_widgets import HLTriggerList as _HLTriggerList
from .list_widgets import ClockList as _ClockList

_dir = _os.path.dirname(_os.path.abspath(__file__))
UI_FILE = _os.path.sep.join([_dir, 'TimingMain.ui'])


def main(prefix=None):
    """Setup the main window."""
    prefix = 'ca://' + (prefix or PREFIX)
    HLTiming = _uic.loadUi(UI_FILE)
    _setupEVGParams(prefix, HLTiming)
    # HLTiming.setStyleSheet('font-size: 21px')

    main = HLTiming.DWCClocks
    map_ = {'Clocks': sorted(_Clocks.HL2LL_MAP.keys())}
    pref = prefix + _Clocks.HL_PREF
    _setupLists(pref, main, map_, listType='clock')

    map_ = {
        'Injection': ('Linac', 'InjBO', 'RmpBO', 'InjSI'),
        'Diagnostics': ('DigLI', 'DigTB', 'DigBO', 'DigTS', 'DigSI'),
        'Storage Ring Control': ('Orbit', 'Tunes', 'Coupl', 'Study'),
        }
    main = HLTiming.DWCEvents
    pref = prefix + _Events.HL_PREF
    _setupLists(pref, main, map_, listType='event')

    map_ = {
        'Linac': (
            'LI-01:TI-EGun:MultBun', 'LI-01:TI-EGun:SglBun',
            'LI-01:TI-Modltr-1:', 'LI-01:TI-Modltr-2:',
            'LI-Glob:TI-LLRF-1:', 'LI-Glob:TI-LLRF-2:',
            'LI-Glob:TI-LLRF-3:', 'LI-Glob:TI-RFAmp-1:',
            'LI-Glob:TI-RFAmp-2:', 'LI-Glob:TI-SHAmp:'),
        'Booster Injection': ('TB-04:TI-InjS:', 'BO-01D:TI-InjK:'),
        }
    main = HLTiming.WDTrigsInjLITB
    _setupLists(prefix, main, map_)

    map_ = {
        'Booster Ramping': ('BO-05D:TI-P5Cav:', 'BO-Glob:TI-Mags:'),
        'Storage Ring Injection': (
            'BO-48D:TI-EjeK:', 'TS-04:TI-InjSF:',
            'TS-Fam:TI-EjeS:', 'TS-Fam:TI-InjSG:',
            'SI-01SA:TI-InjK:'),
        }
    main = HLTiming.WDTrigsInjBOSI
    _setupLists(prefix, main, map_)

    map_ = {
        'Linac': (
            'LI-01:TI-ICT-1:', 'LI-01:TI-ICT-2:',
            'LI-Fam:TI-BPM:', 'LI-Fam:TI-Scrn:'),
        'Booster Transfer Line': (
            'TB-02:TI-ICT:', 'TB-04:TI-FCT:', 'TB-04:TI-ICT:',
            'TB-Fam:TI-BPM:', 'TB-Fam:TI-Scrn:'),
        'Booster': (
            'BO-02D:TI-TuneS:', 'BO-04D:TI-TuneP:', 'BO-04U:TI-GSL:',
            'BO-35D:TI-DCCT:', 'BO-Fam:TI-BPM:', 'BO-Fam:TI-Scrn:'),
        'Storage Ring Injection': (
            'TS-01:TI-ICT:', 'TS-04:TI-FCT:', 'TS-04:TI-ICT:',
            'TS-Fam:TI-BPM:', 'TS-Fam:TI-Scrn:',
            'SI-Fam:TI-BPM:'),
        }
    main = HLTiming.WDTrigsInjDig
    _setupLists(prefix, main, map_)

    map_ = {
        'Storage Ring Studies': (
            'SI-01SA:TI-HPing:', 'SI-01SA:TI-HTuneS:', 'SI-13C4:TI-DCCT:',
            'SI-14C4:TI-DCCT:', 'SI-16C4:TI-GBPM:', 'SI-17C4:TI-VTuneP:',
            'SI-17SA:TI-HTuneP:', 'SI-18C4:TI-VTuneS:', 'SI-19C4:TI-VPing:',
            'SI-19SP:TI-GSL15:', 'SI-20SB:TI-GSL07:'),
        'Storage Ring Magnets': (
            'SI-Glob:TI-Corrs:', 'SI-Glob:TI-Dips:', 'SI-Glob:TI-Quads:',
            'SI-Glob:TI-Sexts:', 'SI-Glob:TI-Skews:',
            )
        }
    main = HLTiming.WDTrigsSI
    _setupLists(prefix, main, map_)
    return HLTiming


def _setupLists(prefix, main, map_, listType='Trig'):
    props = set()
    if listType.lower().startswith('trig'):
        ListClass = _HLTriggerList
        props = {
            'detailed', 'status', 'state', 'source',
            'pulses', 'duration', 'delay'
            }
    elif listType.lower().startswith('ev'):
        ListClass = _EventList
    elif listType.lower().startswith('cl'):
        ListClass = _ClockList

    lv = _QVBoxLayout()
    main.setLayout(lv)
    lv.addItem(_QSpIt(40, 20, _QSzPol.Minimum, _QSzPol.Expanding))
    for name, obj_names in map_.items():
        hl_obj = ListClass(
            name=name, parent=main, prefix=prefix, props=props,
            obj_names=obj_names)
        lv.addWidget(hl_obj)
        lv.addItem(_QSpIt(40, 20, _QSzPol.Minimum, _QSzPol.Expanding))


def _setupEVGParams(prefix, HLTiming):
    pv_pref = prefix + 'AS-Glob:TI-EVG:'
    HLTiming.PyDMWfTBucketListSP.channel = pv_pref + 'BucketList-SP'
    HLTiming.PyDMWfTBucketListRB.channel = pv_pref + 'BucketList-RB'
    HLTiming.PyDMStBContinuous.channel = pv_pref + 'ContinuousEvt-Sel'
    HLTiming.PyDMLedContinuous.channel = pv_pref + 'ContinuousEvt-Sts'
    HLTiming.PyDMStBInjectionState.channel = pv_pref + 'InjectionEvt-Sel'
    HLTiming.PyDMLedInjectionState.channel = pv_pref + 'InjectionEvt-Sts'
    HLTiming.PyDMCbInjectionCyc.channel = pv_pref + 'RepeatBucketList-SP'
    HLTiming.PyDMLedInjectionCyc.channel = pv_pref + 'RepeatBucketList-RB'
    HLTiming.PyDMSBRepetitionRate.channel = pv_pref + 'RepRate-SP'
    HLTiming.PyDMLbRepetitionRate.channel = pv_pref + 'RepRate-RB'


if __name__ == '__main__':
    """Run Example."""
    app = _PyDMApplication()
    HLTiming = main()
    HLTiming.show()
    _sys.exit(app.exec_())
