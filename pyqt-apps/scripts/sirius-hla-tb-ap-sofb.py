#!/usr/bin/env python-sirius

"""TB SOFB Application."""

import sys
import argparse as _argparse
from siriushla.sirius_application import SiriusApplication
from siriuspy.envars import VACA_PREFIX
from siriushla.as_ap_sofb import MainWindow


parser = _argparse.ArgumentParser(description="Run SOFB HLA Interface.")
parser.add_argument(
    '-p', "--prefix", type=str, default=VACA_PREFIX,
    help="Define the prefix for the PVs in the window.")
args = parser.parse_args()

app = SiriusApplication()
app.open_window(MainWindow, parent=None, prefix=args.prefix, acc='TB')
sys.exit(app.exec_())
