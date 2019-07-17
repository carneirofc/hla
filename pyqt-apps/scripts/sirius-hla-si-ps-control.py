#!/usr/bin/env python-sirius

"""SI PS Application."""

import sys
import argparse as _argparse
from siriushla.sirius_application import SiriusApplication

try:
    from siriushla.as_ps_control import PSTabControlWindow, PSControlWindow

    parser = _argparse.ArgumentParser(description="Run SI PS Interface.")
    parser.add_argument('-dev', "--device", type=str, default='')
    args = parser.parse_args()

    device = args.device

    app = SiriusApplication()
    if device:
        window = PSControlWindow
        kwargs = dict(section='SI', discipline='PS', device=device)
    else:
        window = PSTabControlWindow
        kwargs = dict(section='SI', discipline='PS')
    app.open_window(window, parent=None, **kwargs)
    sys.exit(app.exec_())
except:
    app = SiriusApplication()
    app.disclaimer()
