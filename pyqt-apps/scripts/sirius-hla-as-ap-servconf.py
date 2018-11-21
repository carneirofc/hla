#!/usr/bin/env python-sirius

"""Lauch configuration database manager."""
import sys

from siriuspy.servconf.conf_service import ConfigService
from siriushla import util
from siriushla.sirius_application import SiriusApplication
from siriushla.as_ap_servconf.config_server import \
    ConfigurationManager

app = SiriusApplication()
util.set_style(app)
model = ConfigService()
widget = ConfigurationManager(model)
widget.show()
sys.exit(app.exec_())