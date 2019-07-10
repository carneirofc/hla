"""Define Controllers for the orbits displayed in the graphic."""

import pathlib as _pathlib
from datetime import datetime as _datetime
import numpy as _np
from qtpy.QtWidgets import QLabel, QGroupBox, QPushButton, QFormLayout, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QMessageBox, QFileDialog
from qtpy.QtCore import Qt
from pydm.widgets import PyDMLabel, PyDMPushButton, PyDMCheckbox
from siriuspy.csdevice.orbitcorr import ConstTLines
from siriuspy.clientconfigdb import ConfigDBClient, ConfigDBException
from siriushla.widgets.windows import create_window_from_widget
from siriushla.widgets import SiriusLedState, SiriusConnectionSignal
from siriushla.util import connect_window
from siriushla.as_ap_configdb import LoadConfigDialog, SaveConfigDialog

from .respmat_enbllist import SelectionMatrix
from .base import BaseWidget
from ..graphics import SingularValues, ShowMatrixWidget


class RespMatWidget(BaseWidget):

    DEFAULT_DIR = _pathlib.Path.home().as_posix()

    def __init__(self, parent, prefix, acc='SI'):
        super().__init__(parent, prefix, acc=acc)
        self.setupui()
        self._config_type = acc.lower() + '_orbcorr_respm'
        self._client = ConfigDBClient(config_type=self._config_type)
        self.EXT = self._csorb.RESPMAT_FILENAME.split('.')[1]
        self.EXT_FLT = 'RespMat Files (*.{})'.format(self.EXT)
        self.last_dir = self.DEFAULT_DIR

        self._respmat_sp = SiriusConnectionSignal(prefix+'RespMat-SP')
        self._respmat_rb = SiriusConnectionSignal(prefix+'RespMat-RB')

    def channels(self):
        return [self._respmat_sp, self._respmat_rb]

    def setupui(self):
        vbl = QVBoxLayout(self)
        # ####################################################################
        # ####################### Selection Lists ############################
        # ####################################################################
        btns = dict()
        grpbx = QGroupBox('Corrs and BPMs selection', self)
        vbl.addWidget(grpbx)
        szy = 55
        if self.acc == 'BO':
            szy = 32
        elif not self.isring:
            szy = 10
        Window = create_window_from_widget(
            SelectionMatrix, title='Corrs and BPMs selection')
        for dev in ('BPMX', 'BPMY', 'CH', 'CV'):
            btns[dev] = QPushButton(dev, grpbx)
            connect_window(
                btns[dev], Window, self,
                dev=dev, prefix=self.prefix, acc=self.acc)
        gdl = QGridLayout(grpbx)
        # gdl.setSpacing(9)
        gdl.addWidget(btns['BPMX'], 0, 0)
        gdl.addWidget(btns['BPMY'], 1, 0)
        gdl.addWidget(btns['CH'], 0, 1)
        gdl.addWidget(btns['CV'], 1, 1)

        if self.isring:
            pdm_chbx = PyDMCheckbox(
                grpbx, init_channel=self.prefix+'RFEnbl-Sel')
            pdm_chbx.setText('Enable RF')
            pdm_led = SiriusLedState(
                grpbx, init_channel=self.prefix+'RFEnbl-Sts')
            hbl = QHBoxLayout()
            hbl.setContentsMargins(0, 0, 0, 0)
            hbl.addWidget(pdm_chbx)
            hbl.addWidget(pdm_led)
            gdl.addItem(hbl, 2, 1)

        # vbl.addSpacing(40)
        # ####################################################################
        # ######################### Measurement ##############################
        # ####################################################################
        grpbx = QGroupBox('RespMat Measurement', self)
        vbl.addWidget(grpbx)
        pdm_pbtn = PyDMPushButton(
            grpbx, label="Start",
            init_channel=self.prefix+"MeasRespMat-Cmd",
            pressValue=ConstTLines.MeasRespMatCmd.Start)
        pdm_pbtn.setEnabled(True)
        pdm_pbtn2 = PyDMPushButton(
            grpbx, label="Stop",
            init_channel=self.prefix+"MeasRespMat-Cmd",
            pressValue=ConstTLines.MeasRespMatCmd.Stop)
        pdm_pbtn2.setEnabled(True)
        pdm_pbtn3 = PyDMPushButton(
            grpbx, label="Reset",
            init_channel=self.prefix+"MeasRespMat-Cmd",
            pressValue=ConstTLines.MeasRespMatCmd.Reset)
        pdm_pbtn3.setEnabled(True)
        pdm_lbl = PyDMLabel(grpbx, init_channel=self.prefix+'MeasRespMat-Mon')
        pdm_lbl.setAlignment(Qt.AlignCenter)
        gdl = QGridLayout(grpbx)
        # gdl.setSpacing(9)
        gdl.addWidget(pdm_pbtn, 0, 0)
        gdl.addWidget(pdm_pbtn2, 0, 1)
        gdl.addWidget(pdm_pbtn3, 1, 0)
        gdl.addWidget(pdm_lbl, 1, 1)
        gdl.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            2, 0, 1, 2)

        fml = QFormLayout()
        # fml.setSpacing(9)
        gdl.addItem(fml, 3, 0, 1, 2)
        lbl = QLabel('Meas. CH kick [urad]', grpbx)
        wid = self.create_pair(grpbx, 'MeasRespMatKickCH')
        fml.addRow(lbl, wid)
        lbl = QLabel('Meas. CV kick [urad]', grpbx)
        wid = self.create_pair(grpbx, 'MeasRespMatKickCV')
        fml.addRow(lbl, wid)
        if self.isring:
            lbl = QLabel('Meas. RF kick [Hz]', grpbx)
            wid = self.create_pair(grpbx, 'MeasRespMatKickRF')
            fml.addRow(lbl, wid)
        fml.addItem(QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        lbl = QLabel('Wait between kicks [s]', grpbx)
        wid = self.create_pair(grpbx, 'MeasRespMatWait')
        fml.addRow(lbl, wid)

        # vbl.addSpacing(40)
        # ####################################################################
        # ####################### Singular Values ############################
        # ####################################################################
        grpbx = QGroupBox('Singular Values', self)
        vbl.addWidget(grpbx)
        fml = QFormLayout(grpbx)
        lab = QLabel('Nr of SV')
        wid = self.create_pair(grpbx, 'NrSingValues')
        fml.addRow(lab, wid)
        btn = QPushButton('Check Singular Values', grpbx)
        fml.addWidget(btn)
        Window = create_window_from_widget(
            SingularValues, title='Check Singular Values')
        connect_window(btn, Window, grpbx, prefix=self.prefix)
        btn = QPushButton('Check RespMat', grpbx)
        fml.addWidget(btn)
        Window = create_window_from_widget(
            ShowMatrixWidget, title='Check RespMat')
        connect_window(btn, Window, grpbx, prefix=self.prefix, acc=self.acc)

        # vbl.addSpacing(40)
        # ####################################################################
        # ######################## Load/Save/Set #############################
        # ####################################################################
        grpbx = QGroupBox('Load and Save', self)
        vbl.addWidget(grpbx)
        gdl = QGridLayout(grpbx)
        # gdl.setVerticalSpacing(15)
        lbl = QLabel('Load from:', grpbx)
        gdl.addWidget(lbl, 0, 0)
        pbtn = QPushButton('File', grpbx)
        pbtn.clicked.connect(self._load_respmat_from_file)
        gdl.addWidget(pbtn, 0, 1)
        pbtn = QPushButton('ServConf', grpbx)
        pbtn.clicked.connect(self._open_load_config_servconf)
        gdl.addWidget(pbtn, 0, 2)

        lbl = QLabel('Save to:', grpbx)
        gdl.addWidget(lbl, 1, 0)
        pbtn = QPushButton('File', grpbx)
        pbtn.clicked.connect(self._save_respmat_to_file)
        gdl.addWidget(pbtn, 1, 1)
        pbtn = QPushButton('ServConf', grpbx)
        pbtn.clicked.connect(self._open_save_config_servconf)
        gdl.addWidget(pbtn, 1, 2)

    def _save_respmat_to_file(self, _):
        header = '# ' + _datetime.now().strftime('%Y/%m/%d-%H:%M:%S') + '\n'
        if self.isring:
            header += '# (BPMX, BPMY) [um] x (CH, CV, RF) [urad, Hz]' + '\n'
        else:
            header += '# (BPMX, BPMY) [um] x (CH, CV) [urad]' + '\n'
        filename = QFileDialog.getSaveFileName(
            caption='Define a File Name to Save the Response Matrix',
            directory=self.last_dir,
            filter=self.EXT_FLT)
        fname = filename[0]
        if not fname:
            return
        fname += '' if fname.endswith(self.EXT) else ('.' + self.EXT)
        respm = self._respmat_rb.getvalue()
        respm = respm.reshape(-1, self._csorb.NR_CORRS)
        _np.savetxt(fname, respm, header=header)

    def _load_respmat_from_file(self):
        filename = QFileDialog.getOpenFileName(
            caption='Select a Response Matrix File.',
            directory=self.last_dir,
            filter=self.EXT_FLT)
        if not filename[0]:
            return
        respm = _np.loadtxt(filename[0])
        self._respmat_sp.send_value_signal[_np.ndarray].emit(respm.flatten())

    def _open_load_config_servconf(self):
        win = LoadConfigDialog(self._config_type, self)
        win.configname.connect(self._set_respm)
        win.show()

    def _set_respm(self, confname):
        data = self._client.get_config_value(confname)
        self._respmat_sp.send_value_signal[_np.ndarray].emit(
            _np.array(data).flatten())

    def _open_save_config_servconf(self):
        win = SaveConfigDialog(self._config_type, self)
        win.configname.connect(self._save_respm)
        win.show()

    def _save_respm(self, confname):
        val = self._respmat_rb.getvalue()
        val = val.reshape(-1, self._csorb.NR_CORRS)
        try:
            self._client.insert_config(confname, val.tolist())
        except (ConfigDBException, TypeError) as err:
            QMessageBox.warning(self, 'Warning', str(err), QMessageBox.Ok)


def _main():
    app = SiriusApplication()
    win = SiriusDialog()
    hbl = QHBoxLayout(win)
    acc = 'BO'
    prefix = pref+acc+'-Glob:AP-SOFB:'
    wid = RespMatWidget(win, prefix, acc)
    hbl.addWidget(wid)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    from siriushla.sirius_application import SiriusApplication
    from siriushla.widgets import SiriusDialog
    from siriuspy.envars import vaca_prefix as pref
    import sys
    _main()
