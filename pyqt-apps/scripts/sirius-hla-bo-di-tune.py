#!/usr/bin/env python-sirius

"""Interface to handle Booster Tune Measure."""

import sys
import argparse as _argparse
from siriushla.sirius_application import SiriusApplication
from siriuspy.envars import vaca_prefix
from siriushla.as_di_tune import BOTune


parser = _argparse.ArgumentParser(
    description="Run Booster Tune Interface.")
parser.add_argument(
    '-p', "--prefix", type=str, default=vaca_prefix,
    help="Define the prefix for the PVs in the window.")
args = parser.parse_args()

app = SiriusApplication()
app.open_window(BOTune, parent=None, prefix=args.prefix)
sys.exit(app.exec_())