#!/usr/bin/env python-sirius

"""High Level Timming Application."""

import sys
import argparse as _argparse
from siriushla.sirius_application import SiriusApplication
from siriuspy.envars import VACA_PREFIX
from siriushla.widgets.windows import create_window_from_widget
from siriushla.as_ti_control import TimingMain, MonitorWindow


parser = _argparse.ArgumentParser(description="Run Timing HLA Interface.")
parser.add_argument(
    '-p', "--prefix", type=str, default=VACA_PREFIX,
    help="Define the prefix for the PVs in the window.")
parser.add_argument(
    '-t', "--type", type=str, default='main', choices=('main', 'monitor'),
    help="Whether to open monitor window.")
args = parser.parse_args()

app = SiriusApplication(None, sys.argv)
if args.type.lower() == 'main':
    app.open_window(TimingMain, parent=None, prefix=args.prefix)
else:
    window = create_window_from_widget(
        MonitorWindow, title='Timing Monitor', is_main=True)
    app.open_window(window, parent=None, prefix=args.prefix)
sys.exit(app.exec_())
