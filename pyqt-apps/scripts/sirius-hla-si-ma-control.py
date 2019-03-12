#!/usr/bin/env python-sirius

"""SI Magnets Application."""

import sys
import argparse as _argparse
from siriushla.sirius_application import SiriusApplication
from siriushla.as_ps_control import PSTabControlWindow, PSControlWindow

parser = _argparse.ArgumentParser(description="Run SI MA Interface.")
parser.add_argument('-dev', "--device", type=str, default='')
args = parser.parse_args()

device = args.device

app = SiriusApplication()
if device:
    window = PSControlWindow(section='SI', discipline='MA', device=device)
else:
    window = PSTabControlWindow(section='SI', discipline='MA')
window.show()
sys.exit(app.exec_())
