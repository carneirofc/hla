import sys
from pydm import PyDMApplication
from siriusdm.as_config_manager import ConfigManagerWindow


app = PyDMApplication(None, sys.argv)
window = ConfigManagerWindow('SiStrengthPvs')
window.show()
sys.exit(app.exec_())
