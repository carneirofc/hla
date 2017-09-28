#!/usr/bin/env python-sirius

"""TS Position and Angle Correction Application."""

import sys as sys
import argparse as argparse
from pydm import PyDMApplication as PyDMApplication
from siriushla.as_ap_posang.HLPosAng import ASAPPosAngCorr
from siriushla import util


parser = argparse.ArgumentParser(
                    description="Run TS PosAng HLA Interface.")
parser.add_argument('-p', "--prefix", type=str, default='',
                    help="Define the prefix for the PVs in the window.")
args = parser.parse_args()
app = PyDMApplication(None, sys.argv)
util.set_style(app)
window = ASAPPosAngCorr(prefix=args.prefix, tl='ts')
window.show()
sys.exit(app.exec_())