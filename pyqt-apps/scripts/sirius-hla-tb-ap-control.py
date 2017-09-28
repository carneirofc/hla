#!/usr/bin/env python-sirius

"""TB High Level Control Window Application."""

import sys as sys
import argparse as argparse
from pydm import PyDMApplication as PyDMApplication
from siriushla.tl_ap_control.HLTLControl import TLAPControlWindow
from siriushla import util


parser = argparse.ArgumentParser(
                    description="Run TB Control HLA Interface.")
parser.add_argument('-p', "--prefix", type=str, default='',
                    help="Define the prefix for the PVs in the window.")
args = parser.parse_args()

app = PyDMApplication(None, sys.argv)
util.set_style(app)
window = TLAPControlWindow(prefix=args.prefix, tl='tb')
window.show()
sys.exit(app.exec_())