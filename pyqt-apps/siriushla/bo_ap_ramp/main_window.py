"""Booster Ramp Main Window."""

from qtpy.QtCore import Slot, Signal
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QLabel, QWidget, QGridLayout, \
                           QUndoStack, QMessageBox
from siriuspy.ramp import ramp
from siriuspy.clientconfigdb import ConfigDBException as _ConfigDBException
from siriushla.widgets.windows import SiriusMainWindow
from .status_and_commands import StatusAndCommands
from .settings import Settings
from .config_params import ConfigParameters


class RampMain(SiriusMainWindow):
    """Main window of Booster Ramp Control HLA."""

    loadSignal = Signal(ramp.BoosterRamp)

    def __init__(self, parent=None, prefix=''):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Booster Energy Ramping')
        self.prefix = prefix
        self.ramp_config = None
        self._undo_stack = QUndoStack(self)

        self._tunecorr_configname = 'Default'
        self._chromcorr_configname = 'Default'

        self._setupUi()
        self._connSignals()
        self._addActions()

    def _setupUi(self):
        cw = QWidget(self)
        cw.setObjectName('CentralWidget')
        glay = QGridLayout(cw)
        glay.setHorizontalSpacing(10)
        glay.setVerticalSpacing(10)
        lab = QLabel('<h3>Booster Energy Ramping</h3>', cw)
        lab.setStyleSheet("""
            min-height:1.55em; max-height: 1.55em;
            qproperty-alignment: 'AlignVCenter | AlignRight';
            background-color: qlineargradient(spread:pad, x1:1, y1:0.0227273,
                              x2:0, y2:0, stop:0 rgba(173, 190, 207, 255),
                              stop:1 rgba(213, 213, 213, 255));""")
        glay.addWidget(lab, 0, 0, 1, 2)

        self.settings = Settings(
            self, self.prefix, self.ramp_config,
            self._tunecorr_configname, self._chromcorr_configname)
        self.setMenuBar(self.settings)

        self.config_parameters = ConfigParameters(
            self, self.prefix, self.ramp_config, self._undo_stack,
            self._tunecorr_configname, self._chromcorr_configname)
        self.config_parameters.setObjectName('ConfigParameters')
        glay.addWidget(self.config_parameters, 1, 0)

        self.status_and_commands = StatusAndCommands(
            self, self.prefix, self.ramp_config)
        self.status_and_commands.setObjectName('StatusAndCommands')
        glay.addWidget(self.status_and_commands, 1, 1)

        cw.setStyleSheet("""
            #CentralWidget{
                min-width: 144em;
                min-height: 72em;}""")
        glay.setColumnStretch(0, 5)
        glay.setColumnStretch(1, 1)
        self.setCentralWidget(cw)

    def _connSignals(self):
        self.settings.newConfigNameSignal.connect(self._receiveNewConfigName)
        self.settings.loadSignal.connect(self._emitLoadSignal)
        self.settings.opticsSettingsSignal.connect(
            self._handleUpdateOpticsAdjustSettings)
        self.settings.plotUnitSignal.connect(
            self.config_parameters.getPlotUnits)

        self.config_parameters.dip_ramp.updateDipoleRampSignal.connect(
            self._verifySync)
        self.config_parameters.dip_ramp.updateDipoleRampSignal.connect(
            self.config_parameters.mult_ramp.updateTable)
        self.config_parameters.dip_ramp.updateDipoleRampSignal.connect(
            self.config_parameters.mult_ramp.updateGraph)
        self.config_parameters.dip_ramp.updateDipoleRampSignal.connect(
            self.status_and_commands.update_ma_params)
        self.config_parameters.dip_ramp.updateDipoleRampSignal.connect(
            self.status_and_commands.update_ti_params)
        self.config_parameters.mult_ramp.updateMultipoleRampSignal.connect(
            self._verifySync)
        self.config_parameters.mult_ramp.updateMultipoleRampSignal.connect(
            self.status_and_commands.update_ma_params)
        self.config_parameters.rf_ramp.updateRFRampSignal.connect(
            self._verifySync)
        self.config_parameters.rf_ramp.updateRFRampSignal.connect(
            self.status_and_commands.update_rf_params)

        self.loadSignal.connect(self.settings.getRampConfig)
        self.loadSignal.connect(self.config_parameters.handleLoadRampConfig)
        self.loadSignal.connect(
            self.config_parameters.dip_ramp.handleLoadRampConfig)
        self.loadSignal.connect(
            self.config_parameters.mult_ramp.handleLoadRampConfig)
        self.loadSignal.connect(
            self.config_parameters.rf_ramp.handleLoadRampConfig)
        self.loadSignal.connect(self.status_and_commands.handleLoadRampConfig)

    def _addActions(self):
        self.act_undo = self._undo_stack.createUndoAction(self, 'Undo')
        self.act_undo.setShortcut(QKeySequence.Undo)
        self.settings.config_menu.addAction(self.act_undo)
        self.act_redo = self._undo_stack.createRedoAction(self, 'Redo')
        self.act_redo.setShortcut(QKeySequence.Redo)
        self.settings.config_menu.addAction(self.act_redo)

    @Slot(str)
    def _receiveNewConfigName(self, new_config_name):
        self.ramp_config = ramp.BoosterRamp(new_config_name, auto_update=True)
        self._emitLoadSignal()

    def _emitLoadSignal(self):
        try:
            if self.ramp_config.exist():
                self.ramp_config.load()
        except _ConfigDBException as err:
            QMessageBox.critical(self, 'Error', str(err), QMessageBox.Ok)
        else:
            self.loadSignal.emit(self.ramp_config)
        finally:
            self._verifySync()

    def _verifySync(self):
        """Verify sync status related to ConfServer."""
        if self.ramp_config is not None:
            if not self.ramp_config.synchronized:
                self.config_parameters.setStyleSheet(
                    '#ConfigParameters {color: red;}')
                self.config_parameters.setToolTip('There are unsaved changes')
            else:
                self.config_parameters.setStyleSheet('')
                self.config_parameters.setToolTip('')

    def closeEvent(self, ev):
        """Reimplement closeEvent to avoid forgeting saving changes."""
        self.close_ev = ev

        if self.ramp_config is None:
            return self._acceptClose()

        if not self.ramp_config.synchronized:
            ans = QMessageBox.question(
                self, 'Save changes?',
                'There are unsaved changes in {}. \n'
                'Do you want to save?'.format(self.ramp_config.name),
                QMessageBox.Yes, QMessageBox.Cancel)
            if ans == QMessageBox.Yes:
                self._ignoreCloseAndSave()
            else:
                self._acceptClose()

    def _ignoreCloseAndSave(self):
        self.close_ev.ignore()
        self.settings.showSaveAsPopup()

    def _acceptClose(self):
        self.close_ev.accept()
        super().closeEvent(self.close_ev)

    @Slot(str, str)
    def _handleUpdateOpticsAdjustSettings(self, tune_cname, chrom_cname):
        self._tunecorr_configname = tune_cname
        self._chromcorr_configname = chrom_cname
        self.config_parameters.updateOpticsAdjustSettings(
            tune_cname, chrom_cname)


if __name__ == '__main__':
    """Run Example."""
    import sys
    from siriushla.sirius_application import SiriusApplication
    from siriuspy.envars import vaca_prefix as _vaca_prefix

    app = SiriusApplication()
    w = RampMain(prefix=_vaca_prefix)
    w.show()
    sys.exit(app.exec_())
