#!/usr/bin/env python-sirius

"""High Level Application to Current and Lifetime Monitoring."""

import sys as sys
import argparse as argparse
from siriushla.sirius_application import SiriusApplication
from siriushla.as_ap_currlt.HLCurrentLifetime import CurrLTWindow
from siriushla import util


parser = argparse.ArgumentParser(
                    description="Run Current and Lifetime HLA Interface.")
parser.add_argument('-p', "--prefix", type=str, default='',
                    help="Define the prefix for the PVs in the window.")
args = parser.parse_args()

app = SiriusApplication()
util.set_style(app)
window = CurrLTWindow(prefix=args.prefix, acc='bo')
window.show()
sys.exit(app.exec_())
