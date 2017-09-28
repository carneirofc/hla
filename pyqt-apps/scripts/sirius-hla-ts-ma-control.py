#!/usr/bin/env python-sirius

"""TS Magnets Application."""

import sys
from pydm import PyDMApplication
from siriushla.as_ma_control.MagnetTabControlWindow \
    import MagnetTabControlWindow
from siriushla import util


app = PyDMApplication(None, sys.argv)
util.set_style(app)
window = MagnetTabControlWindow(section="TS")
window.show()
sys.exit(app.exec_())
