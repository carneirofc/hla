#!/usr/bin/env python-sirius

"""Power Supply Cycling Application."""

import sys
from siriushla.sirius_application import SiriusApplication
from siriushla.as_ps_cycle.cycle_window import CycleWindow


app = SiriusApplication(None, sys.argv)
app.open_window(CycleWindow)
sys.exit(app.exec_())
