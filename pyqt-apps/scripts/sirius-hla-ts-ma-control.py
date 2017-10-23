#!/usr/bin/env python-sirius

"""TS Magnets Application."""

import sys
from siriushla.SiriusApplication import SiriusApplication
from siriushla.as_ma_control.MagnetTabControlWindow \
    import MagnetTabControlWindow
from siriushla import util


app = SiriusApplication()
util.set_style(app)
window = MagnetTabControlWindow(section="TS")
window.show()
sys.exit(app.exec_())
