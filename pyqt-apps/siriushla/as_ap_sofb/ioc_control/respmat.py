"""Define Controllers for the orbits displayed in the graphic."""

import pathlib as _pathlib
from datetime import datetime as _datetime
import numpy as _np
from qtpy.QtWidgets import QLabel, QGroupBox, QPushButton, QFormLayout, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QMessageBox, QFileDialog, QWidget, QTabWidget
from qtpy.QtCore import Qt
import qtawesome as qta

from pydm.widgets import PyDMLabel, PyDMPushButton, PyDMCheckbox
from siriuspy.sofb.csdev import ConstTLines
from siriuspy.clientconfigdb import ConfigDBClient, ConfigDBException
from siriushla.widgets.windows import create_window_from_widget
from siriushla.widgets import SiriusLedState, SiriusConnectionSignal, \
    SiriusLabel
from siriushla.util import connect_window, get_appropriate_color
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
        self.EXT = self._csorb.respmat_fname.split('.')[1]
        self.EXT_FLT = 'RespMat Files (*.{})'.format(self.EXT)
        self.last_dir = self.DEFAULT_DIR

        self._respmat_sp = SiriusConnectionSignal(prefix+'RespMat-SP')
        self._respmat_rb = SiriusConnectionSignal(prefix+'RespMat-RB')

    def setupui(self):
        """."""
        gbox = QGroupBox('Matrix', self)
        gbox.setObjectName('grbx')
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(gbox)
        vbl = QVBoxLayout(gbox)
        tabw = QTabWidget(gbox)
        vbl.addWidget(tabw)

        main_wid = self.get_main_widget(tabw)
        tabw.addTab(main_wid, 'Main')

        svs_wid = self.get_singular_values_widget(tabw)
        tabw.addTab(svs_wid, 'SVs')

        meas_wid = self.get_measurement_widget(tabw)
        tabw.addTab(meas_wid, 'Meas')

    def get_main_widget(self, parent):
        main_wid = QWidget(parent)
        main_lay = QVBoxLayout(main_wid)
        main_lay.setContentsMargins(0, 0, 0, 0)

        sel_gp = QGroupBox('Sel.')
        sel_gp.setLayout(QHBoxLayout())
        sel_gp.layout().setContentsMargins(0, 0, 0, 0)
        sel_wid = self.get_selection_lists_widget(sel_gp)
        sel_gp.layout().addWidget(sel_wid)
        main_lay.addWidget(sel_gp)

        svld_gp = QGroupBox('Load and Save')
        svld_gp.setLayout(QHBoxLayout())
        svld_gp.layout().setContentsMargins(0, 0, 0, 0)
        svld_wid = self.get_saveload_widget(svld_gp)
        svld_gp.layout().addWidget(svld_wid)
        main_lay.addWidget(svld_gp)

        return main_wid

    def get_selection_lists_widget(self, parent):
        """."""
        sel_wid = QWidget(parent)
        sel_lay = QHBoxLayout(sel_wid)

        icon = qta.icon('fa5s.hammer', color=get_appropriate_color(self.acc))
        Window = create_window_from_widget(
            SelectionMatrix, title='Corrs and BPMs selection', icon=icon)
        btn = QPushButton('', sel_wid)
        btn.setObjectName('btn')
        btn.setIcon(qta.icon('fa5s.tasks'))
        btn.setToolTip('Open window to select BPMs and correctors')
        btn.setStyleSheet(
            '#btn{min-width:3.8em; max-width:3.8em;\
            min-height:2em; max-height:2em; icon-size:25px;}')
        connect_window(btn, Window, None, prefix=self.prefix, acc=self.acc)
        sel_lay.addWidget(btn)

        if self.acc == 'SI':
            pdm_chbx = PyDMCheckbox(
                sel_wid, init_channel=self.prefix+'RFEnbl-Sel')
            pdm_chbx.setText('use RF')
            pdm_led = SiriusLedState(
                sel_wid, init_channel=self.prefix+'RFEnbl-Sts')
            sel_lay.addStretch()
            sel_lay.addWidget(pdm_chbx)
            sel_lay.addWidget(pdm_led)

        btn = QPushButton('', sel_wid)
        btn.setToolTip('Visualize RespMat')
        btn.setIcon(qta.icon('mdi.chart-line'))
        btn.setObjectName('btn')
        btn.setStyleSheet('#btn{max-width:40px; icon-size:40px;}')
        Window = create_window_from_widget(
            ShowMatrixWidget, title='Check RespMat')
        connect_window(btn, Window, sel_wid, prefix=self.prefix, acc=self.acc)
        sel_lay.addWidget(btn)

        return sel_wid

    def get_singular_values_widget(self, parent):
        """."""
        svs_wid = QWidget(parent)
        svs_lay = QGridLayout(svs_wid)

        wid = self.create_pair(svs_wid, 'MinSingValue')
        lbl = QLabel('Min. SV: ')
        svs_lay.addWidget(lbl, 0, 0)
        svs_lay.addWidget(wid, 0, 1)

        wid = self.create_pair(svs_wid, 'TikhonovRegConst')
        lbl = QLabel('Tikhonov: ')
        svs_lay.addWidget(lbl, 1, 0)
        svs_lay.addWidget(wid, 1, 1)

        lbl = QLabel('Nr Sing Vals')
        lbls = SiriusLabel(
            svs_wid, init_channel=self.prefix+'NrSingValues-Mon')
        btn = QPushButton('', svs_wid)
        btn.setToolTip('Check Singular Values')
        btn.setIcon(qta.icon('mdi.chart-line'))
        btn.setObjectName('btn')
        btn.setStyleSheet('#btn{max-width:30px; icon-size:30px;}')
        hbl = QHBoxLayout()
        hbl.addWidget(btn)
        hbl.addStretch()
        hbl.addWidget(lbl)
        hbl.addWidget(lbls)
        svs_lay.addLayout(hbl, 2, 0, 1, 2)

        Window = create_window_from_widget(
            SingularValues, title='Check Singular Values')
        connect_window(btn, Window, svs_wid, prefix=self.prefix)

        return svs_wid

    def get_measurement_widget(self, parent):
        """."""
        meas_wid = QWidget(parent)
        meas_lay = QVBoxLayout(meas_wid)

        strt = PyDMPushButton(
            meas_wid,
            init_channel=self.prefix+"MeasRespMat-Cmd",
            pressValue=ConstTLines.MeasRespMatCmd.Start)
        strt.setEnabled(True)
        strt.setToolTip('Start Measurement')
        strt.setIcon(qta.icon('fa5s.play'))
        strt.setObjectName('strt')
        strt.setStyleSheet(
            '#strt{min-width:25px; max-width:25px; icon-size:20px;}')
        stop = PyDMPushButton(
            meas_wid,
            init_channel=self.prefix+"MeasRespMat-Cmd",
            pressValue=ConstTLines.MeasRespMatCmd.Stop)
        stop.setEnabled(True)
        stop.setToolTip('Stop Measurement')
        stop.setIcon(qta.icon('fa5s.stop'))
        stop.setObjectName('stop')
        stop.setStyleSheet(
            '#stop{min-width:25px; max-width:25px; icon-size:20px;}')
        rst = PyDMPushButton(
            meas_wid,
            init_channel=self.prefix+"MeasRespMat-Cmd",
            pressValue=ConstTLines.MeasRespMatCmd.Reset)
        rst.setEnabled(True)
        rst.setToolTip('Reset Measurement Status')
        rst.setIcon(qta.icon('fa5s.sync'))
        rst.setObjectName('conf')
        rst.setStyleSheet(
            '#conf{min-width:25px; max-width:25px; icon-size:20px;}')
        lbl = PyDMLabel(meas_wid, init_channel=self.prefix+'MeasRespMat-Mon')
        lbl.setAlignment(Qt.AlignCenter)
        hbl = QHBoxLayout()
        hbl.setSpacing(8)
        meas_lay.addItem(hbl)
        hbl.addWidget(strt)
        hbl.addWidget(stop)
        hbl.addWidget(rst)
        hbl.addStretch()
        hbl.addWidget(lbl)

        fml = QFormLayout()
        meas_lay.addSpacing(20)
        meas_lay.addItem(fml)
        lbl = QLabel('CH [urad]', meas_wid)
        wid = self.create_pair(meas_wid, 'MeasRespMatKickCH')
        fml.addRow(lbl, wid)
        lbl = QLabel('CV [urad]', meas_wid)
        wid = self.create_pair(meas_wid, 'MeasRespMatKickCV')
        fml.addRow(lbl, wid)
        if self.acc == 'SI':
            lbl = QLabel('RF [Hz]', meas_wid)
            wid = self.create_pair(meas_wid, 'MeasRespMatKickRF')
            fml.addRow(lbl, wid)
        lbl = QLabel('Wait [s]', meas_wid)
        lbl.setToolTip('Time to wait between kicks')
        wid = self.create_pair(meas_wid, 'MeasRespMatWait')
        fml.addRow(lbl, wid)

        return meas_wid

    def get_saveload_widget(self, parent):
        """."""
        svld_wid = QWidget(parent)
        svld_lay = QGridLayout(svld_wid)

        lbl = QLabel('Load:', svld_wid)
        svld_lay.addWidget(lbl, 0, 0, alignment=Qt.AlignRight)
        pbtn = QPushButton('', svld_wid)
        pbtn.setIcon(qta.icon('mdi.file-upload-outline'))
        pbtn.setToolTip('Load RespMat from file')
        pbtn.clicked.connect(self._load_respmat_from_file)
        svld_lay.addWidget(pbtn, 0, 1)
        pbtn = QPushButton('', svld_wid)
        pbtn.setIcon(qta.icon('mdi.cloud-upload-outline'))
        pbtn.setToolTip('Load RespMat from ServConf')
        pbtn.clicked.connect(self._open_load_config_servconf)
        svld_lay.addWidget(pbtn, 0, 2)

        lbl = QLabel('Save:', svld_wid)
        svld_lay.addWidget(lbl, 0, 3, alignment=Qt.AlignRight)
        pbtn = QPushButton('', svld_wid)
        pbtn.setIcon(qta.icon('mdi.file-download-outline'))
        pbtn.setToolTip('Save RespMat to file')
        pbtn.clicked.connect(self._save_respmat_to_file)
        svld_lay.addWidget(pbtn, 0, 4)
        pbtn = QPushButton('', svld_wid)
        pbtn.setIcon(qta.icon('mdi.cloud-download-outline'))
        pbtn.setToolTip('Save RespMat to ServConf')
        pbtn.clicked.connect(self._open_save_config_servconf)
        svld_lay.addWidget(pbtn, 0, 5)
        self.respmat_label = QLabel('')
        svld_lay.addWidget(self.respmat_label, 1, 0, 1, 5)

        svld_lay.setRowStretch(2, 10)
        return svld_wid

    def _save_respmat_to_file(self, _):
        header = '# ' + _datetime.now().strftime('%Y/%m/%d-%H:%M:%S') + '\n'
        if self.acc == 'SI':
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
        respm = respm.reshape(-1, self._csorb.nr_corrs)
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
        self.respmat_label.setText('Loaded from file: \n\n' + filename[0])

    def _open_load_config_servconf(self):
        win = LoadConfigDialog(self._config_type, self)
        win.configname.connect(self._set_respm)
        win.show()

    def _set_respm(self, confname):
        data = self._client.get_config_value(confname)
        self._respmat_sp.send_value_signal[_np.ndarray].emit(
            _np.array(data).flatten())
        self.respmat_label.setText('Loaded from ServConf: \n\n' + confname)

    def _open_save_config_servconf(self):
        win = SaveConfigDialog(self._config_type, self)
        win.configname.connect(self._save_respm)
        win.show()

    def _save_respm(self, confname):
        val = self._respmat_rb.getvalue()
        val = val.reshape(-1, self._csorb.nr_corrs)
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
    from siriuspy.envars import VACA_PREFIX as pref
    import sys
    _main()
