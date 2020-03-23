#!/usr/bin/env python-sirius

"""HLA as_ap_posang module."""

import os as _os
from epics import PV as _PV
from qtpy.QtWidgets import QGridLayout, QLabel, QGroupBox, QAbstractItemView, \
    QSizePolicy as QSzPlcy, QSpacerItem, QPushButton, QHeaderView, QWidget
from qtpy.QtCore import Qt
import qtawesome as qta

from siriuspy.envars import VACA_PREFIX as _VACA_PREFIX
from siriuspy.csdevice.posang import Const
from siriuspy.namesys import SiriusPVName as _PVName

from pydm.widgets import PyDMWaveformTable, PyDMLabel, PyDMLineEdit, \
    PyDMPushButton, PyDMSpinbox

from siriushla import util as _hlautil
from siriushla.widgets import SiriusMainWindow, PyDMLogLabel, SiriusLedAlert, \
    PyDMLinEditScrollbar, PyDMLedMultiChannel
from siriushla.as_ps_control import PSDetailWindow as _PSDetailWindow
from siriushla.as_pu_control import PUDetailWindow as _PUDetailWindow
from siriushla.as_ap_configdb import LoadConfigDialog as _LoadConfigDialog


UI_FILE = (_os.path.abspath(_os.path.dirname(__file__))+'/ui_as_ap_posang.ui')


class PosAngCorr(SiriusMainWindow):
    """Main Class."""

    def __init__(self, parent=None, prefix='', tl=None):
        """Class construc."""
        super(PosAngCorr, self).__init__(parent)
        if not prefix:
            self._prefix = _VACA_PREFIX
        else:
            self._prefix = prefix
        self._tl = tl.upper()
        self.posang_prefix = self._prefix + self._tl + '-Glob:AP-PosAng'
        self.setObjectName(self._tl+'App')
        self.setWindowTitle(self._tl + ' Position and Angle Correction Window')

        if self._tl == 'TS':
            self._is_chsept = False
            ch3_pv = _PV(self.posang_prefix+':CH3-Cte',
                         connection_timeout=0.1)
            if not ch3_pv.wait_for_connection():
                self._is_chsept = True

        if tl == 'ts':
            CORRH = (Const.TS_CORRH_POSANG_CHSEPT if self._is_chsept
                     else Const.TS_CORRH_POSANG_SEPTSEPT)
            CORRV = Const.TS_CORRV_POSANG
        elif tl == 'tb':
            CORRH = Const.TB_CORRH_POSANG
            CORRV = Const.TB_CORRV_POSANG

        self.corrs = dict()
        self.corrs['CH1'] = _PVName(CORRH[0])
        self.corrs['CH2'] = _PVName(CORRH[1])
        if len(CORRH) == 3:
            self.corrs['CH3'] = _PVName(CORRH[2])
        self.corrs['CV1'] = _PVName(CORRV[0])
        self.corrs['CV2'] = _PVName(CORRV[1])

        self._setupUi()
        self.setFocus(True)
        self.setFocusPolicy(Qt.StrongFocus)

    def _setupUi(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)

        # label
        lab = QLabel(
            '<h3>'+self._tl+' Position and Angle Correction</h3>', cw)
        lab.setStyleSheet("""
            min-height:1.55em; max-height: 1.55em;
            qproperty-alignment: 'AlignVCenter | AlignRight';
            background-color: qlineargradient(spread:pad, x1:1, y1:0.0227273,
                              x2:0, y2:0, stop:0 rgba(173, 190, 207, 255),
                              stop:1 rgba(213, 213, 213, 255));""")

        # apply button
        self.pb_updateref = PyDMPushButton(
            self, 'Update Reference', pressValue=1,
            init_channel=self.posang_prefix+':SetNewRefKick-Cmd')
        self.pb_updateref.setStyleSheet(
            'min-height: 2.4em; max-height: 2.4em;')

        # delta setters
        self.hgbox = QGroupBox('Horizontal', self)
        self.hgbox.setLayout(self._setupDeltaControlLayout('x'))

        self.vgbox = QGroupBox('Vertical', self)
        self.vgbox.setLayout(self._setupDeltaControlLayout('y'))

        # correctors
        self.corrgbox = QGroupBox('Correctors', self)
        self.corrgbox.setLayout(self._setupCorrectorsLayout())

        # status
        self.statgbox = QGroupBox('Correction Status', self)
        self.statgbox.setLayout(self._setupStatusLayout())

        glay = QGridLayout(cw)
        glay.setHorizontalSpacing(12)
        glay.setVerticalSpacing(12)
        glay.addWidget(lab, 0, 0, 1, 2)
        glay.addWidget(self.pb_updateref, 1, 0, 1, 2)
        glay.addWidget(self.hgbox, 2, 0)
        glay.addWidget(self.vgbox, 2, 1)
        glay.addWidget(self.corrgbox, 3, 0, 1, 2)
        glay.addWidget(self.statgbox, 4, 0, 1, 2)

        # menu
        act_settings = self.menuBar().addAction('Settings')
        _hlautil.connect_window(act_settings, CorrParamsDetailWindow,
                                parent=self, tl=self._tl, prefix=self._prefix)

        # stlesheet
        self.setStyleSheet("""
            PyDMSpinbox{
                min-width: 5em; max-width: 5em;
            }
            PyDMLabel, PyDMLinEditScrollbar{
                min-width: 6em; max-width: 6em;
            }
            QPushButton{
                min-width: 8em;
            }
            QLabel{
                min-height: 1.35em;
                qproperty-alignment: AlignCenter;
            }
        """)

    def _setupDeltaControlLayout(self, axis=''):
        # pos
        label_pos = QLabel("<h4>Δ"+axis+"</h4>", self)
        sb_deltapos = PyDMSpinbox(
            self, self.posang_prefix + ':DeltaPos'+axis.upper()+'-SP')
        sb_deltapos.showStepExponent = False
        lb_deltapos = PyDMLabel(
            self, self.posang_prefix + ':DeltaPos'+axis.upper()+'-RB')
        lb_deltapos.showUnits = True
        # ang
        label_ang = QLabel("<h4>Δ"+axis+"'</h4>", self)
        sb_deltaang = PyDMSpinbox(
            self, self.posang_prefix + ':DeltaAng'+axis.upper()+'-SP')
        sb_deltaang.showStepExponent = False
        lb_deltaang = PyDMLabel(
            self, self.posang_prefix + ':DeltaAng'+axis.upper()+'-RB')
        lb_deltaang.showUnits = True

        lay = QGridLayout()
        lay.setVerticalSpacing(12)
        lay.setHorizontalSpacing(12)
        lay.addItem(
            QSpacerItem(10, 0, QSzPlcy.Expanding, QSzPlcy.Ignored), 0, 0)
        lay.addWidget(label_pos, 0, 1)
        lay.addWidget(sb_deltapos, 0, 2)
        lay.addWidget(lb_deltapos, 0, 3)
        lay.addWidget(label_ang, 1, 1)
        lay.addWidget(sb_deltaang, 1, 2)
        lay.addWidget(lb_deltaang, 1, 3)
        lay.addItem(
            QSpacerItem(10, 0, QSzPlcy.Expanding, QSzPlcy.Ignored), 0, 4)
        return lay

    def _setupCorrectorsLayout(self):
        lay = QGridLayout()
        lay.setVerticalSpacing(9)
        lay.setHorizontalSpacing(9)

        label_kicksp = QLabel('<h4>Kick-SP</h4>', self)
        label_kickrb = QLabel('<h4>Kick-RB</h4>', self)
        label_kickref = QLabel('<h4>RefKick-Mon</h4>', self)
        lay.addWidget(label_kicksp, 0, 2)
        lay.addWidget(label_kickrb, 0, 3)
        lay.addWidget(label_kickref, 0, 4)

        idx = 1
        for corrid, corr in self.corrs.items():
            pb = QPushButton(qta.icon('fa5s.list-ul'), '', self)
            pb.setObjectName('pb')
            pb.setStyleSheet("""
                #pb{
                    min-width:25px; max-width:25px;
                    min-height:25px; max-height:25px;
                    icon-size:20px;}
                """)
            if corr.dis == 'PU':
                _hlautil.connect_window(
                    pb, _PUDetailWindow, self, devname=corr)
            else:
                _hlautil.connect_window(
                    pb, _PSDetailWindow, self, psname=corr)
            lb_name = QLabel(corr, self)
            le_sp = PyDMLinEditScrollbar(self._prefix+corr+':Kick-SP', self)
            le_sp.layout.setContentsMargins(0, 0, 0, 0)
            le_sp.layout.setSpacing(3)
            le_sp.setSizePolicy(QSzPlcy.Minimum, QSzPlcy.Maximum)
            le_sp.sp_lineedit.setStyleSheet("min-height:1.29em;")
            le_sp.sp_lineedit.setAlignment(Qt.AlignCenter)
            le_sp.sp_lineedit.setSizePolicy(QSzPlcy.Ignored, QSzPlcy.Fixed)
            le_sp.sp_scrollbar.setStyleSheet("max-height:0.7em;")
            le_sp.sp_scrollbar.limitsFromPV = True
            lb_rb = PyDMLabel(self, self._prefix+corr+':Kick-RB')
            lb_ref = PyDMLabel(
                self, self.posang_prefix+':RefKick'+corrid+'-Mon')

            lay.addWidget(pb, idx, 0, alignment=Qt.AlignTop)
            lay.addWidget(
                lb_name, idx, 1, alignment=Qt.AlignLeft | Qt.AlignTop)
            lay.addWidget(le_sp, idx, 2, alignment=Qt.AlignTop)
            lay.addWidget(lb_rb, idx, 3, alignment=Qt.AlignTop)
            lay.addWidget(lb_ref, idx, 4, alignment=Qt.AlignTop)
            idx += 1

        if self._tl == 'TB':
            lay.addItem(QSpacerItem(0, 8, QSzPlcy.Ignored, QSzPlcy.Fixed))

            label_voltsp = QLabel('<h4>Amplitude-SP</h4>', self)
            label_voltrb = QLabel('<h4>Amplitude-RB</h4>', self)
            lay.addWidget(label_voltsp, idx+2, 2)
            lay.addWidget(label_voltrb, idx+2, 3)

            lb_kly2_name = QLabel('Klystron 2', self)
            le_kly2_sp = PyDMLinEditScrollbar('LA-RF:LLRF:KLY2:SET_AMP', self)
            le_kly2_sp.layout.setContentsMargins(0, 0, 0, 0)
            le_kly2_sp.layout.setSpacing(3)
            le_kly2_sp.setSizePolicy(QSzPlcy.Minimum, QSzPlcy.Maximum)
            le_kly2_sp.sp_lineedit.setStyleSheet("min-height:1.29em;")
            le_kly2_sp.sp_lineedit.precisionFromPV = False
            le_kly2_sp.sp_lineedit.precision = 2
            le_kly2_sp.sp_lineedit.setAlignment(Qt.AlignCenter)
            le_kly2_sp.sp_lineedit.setSizePolicy(
                QSzPlcy.Ignored, QSzPlcy.Fixed)
            le_kly2_sp.sp_scrollbar.setStyleSheet("max-height:0.7em;")
            le_kly2_sp.sp_scrollbar.limitsFromPV = True
            lb_kly2_rb = PyDMLabel(self, 'LA-RF:LLRF:KLY2:GET_AMP')
            lb_kly2_rb.precisionFromPV = False
            lb_kly2_rb.precision = 2
            lay.addWidget(lb_kly2_name, idx+3, 1,
                          alignment=Qt.AlignLeft | Qt.AlignTop)
            lay.addWidget(le_kly2_sp, idx+3, 2, alignment=Qt.AlignTop)
            lay.addWidget(lb_kly2_rb, idx+3, 3, alignment=Qt.AlignTop)
            self._kckr_name = 'BO-01D:PU-InjKckr'
        else:
            self._kckr_name = 'SI-01SA:PU-InjNLKckr'

        label_voltsp = QLabel('<h4>Voltage-SP</h4>', self)
        label_voltrb = QLabel('<h4>Voltage-RB</h4>', self)
        lay.addWidget(label_voltsp, idx+4, 2)
        lay.addWidget(label_voltrb, idx+4, 3)

        lay.addItem(QSpacerItem(0, 8, QSzPlcy.Ignored, QSzPlcy.Fixed))
        pb_kckr = QPushButton(qta.icon('fa5s.list-ul'), '', self)
        pb_kckr.setObjectName('pb')
        pb_kckr.setStyleSheet("""
            #pb{
                min-width:25px; max-width:25px;
                min-height:25px; max-height:25px;
                icon-size:20px;}
            """)
        lb_kckr_name = QLabel(self._kckr_name, self)
        _hlautil.connect_window(
            pb_kckr, _PUDetailWindow, self, devname=self._kckr_name)
        lb_kckr_sp = PyDMLinEditScrollbar(self._kckr_name+':Voltage-SP', self)
        lb_kckr_sp.layout.setContentsMargins(0, 0, 0, 0)
        lb_kckr_sp.layout.setSpacing(3)
        lb_kckr_sp.setSizePolicy(QSzPlcy.Minimum, QSzPlcy.Maximum)
        lb_kckr_sp.sp_lineedit.setStyleSheet("min-height:1.29em;")
        lb_kckr_sp.sp_lineedit.setAlignment(Qt.AlignCenter)
        lb_kckr_sp.sp_lineedit.setSizePolicy(QSzPlcy.Ignored, QSzPlcy.Fixed)
        lb_kckr_sp.sp_scrollbar.setStyleSheet("max-height:0.7em;")
        lb_kckr_sp.sp_scrollbar.limitsFromPV = True
        lb_kckr_rb = PyDMLabel(self, self._kckr_name+':Voltage-RB')
        lay.addWidget(pb_kckr, idx+5, 0, alignment=Qt.AlignTop)
        lay.addWidget(
            lb_kckr_name, idx+5, 1, alignment=Qt.AlignLeft | Qt.AlignTop)
        lay.addWidget(lb_kckr_sp, idx+5, 2, alignment=Qt.AlignTop)
        lay.addWidget(lb_kckr_rb, idx+5, 3, alignment=Qt.AlignTop)
        return lay

    def _setupStatusLayout(self):
        self.log = PyDMLogLabel(self, self.posang_prefix+':Log-Mon')
        self.lb_sts0 = QLabel(Const.STATUSLABELS[0], self)
        self.led_sts0 = SiriusLedAlert(
            self, self.posang_prefix+':Status-Mon', bit=0)
        self.lb_sts1 = QLabel(Const.STATUSLABELS[1], self)
        self.led_sts1 = SiriusLedAlert(
            self, self.posang_prefix+':Status-Mon', bit=1)
        self.lb_sts2 = QLabel(Const.STATUSLABELS[2], self)
        self.led_sts2 = SiriusLedAlert(
            self, self.posang_prefix+':Status-Mon', bit=2)
        self.lb_sts3 = QLabel(Const.STATUSLABELS[3], self)
        self.led_sts3 = SiriusLedAlert(
            self, self.posang_prefix+':Status-Mon', bit=3)
        self.pb_config = PyDMPushButton(
            self, label='Config Correctors', pressValue=1,
            init_channel=self.posang_prefix+':ConfigPS-Cmd')

        lay = QGridLayout()
        lay.setVerticalSpacing(12)
        lay.setHorizontalSpacing(12)
        lay.addWidget(self.log, 0, 0, 6, 1)
        lay.addWidget(self.lb_sts0, 1, 2)
        lay.addWidget(self.led_sts0, 1, 1)
        lay.addWidget(self.lb_sts1, 2, 2)
        lay.addWidget(self.led_sts1, 2, 1)
        lay.addWidget(self.lb_sts2, 3, 2)
        lay.addWidget(self.led_sts2, 3, 1)
        lay.addWidget(self.lb_sts3, 4, 2)
        lay.addWidget(self.led_sts3, 4, 1)
        lay.addWidget(self.pb_config, 5, 1, 1, 2)

        if self._tl == 'TS':
            self.led_corrtype = PyDMLedMultiChannel(
                self, {self.posang_prefix+':CH1-Cte': self.corrs['CH1']})
            self.lb_corrtype = QLabel(
                'Control ' + ('CH-Sept' if self._is_chsept else 'Sept-Sept'))
            lay.addWidget(self.led_corrtype, 0, 1)
            lay.addWidget(self.lb_corrtype, 0, 2)
        return lay

    def _set_correctors_channels(self, corrs):
        self.centralwidget.pushButton_CH1.setText(corrs[0])
        _hlautil.connect_window(
            self.centralwidget.pushButton_CH1, _PSDetailWindow, self,
            psname=corrs[0])
        self.centralwidget.PyDMLabel_KickRBCH1.channel = (
            self._prefix + corrs[0] + ':Kick-RB')

        self.centralwidget.pushButton_CH2.setText(corrs[1])
        if corrs[1].dis == 'PU':
            _hlautil.connect_window(
                self.centralwidget.pushButton_CH2, _PUDetailWindow, self,
                devname=corrs[1])
        else:
            _hlautil.connect_window(
                self.centralwidget.pushButton_CH2, _PSDetailWindow, self,
                psname=corrs[1])
        self.centralwidget.PyDMLabel_KickRBCH2.channel = (
            self._prefix + corrs[1] + ':Kick-RB')

        self.centralwidget.pushButton_CV1.setText(corrs[2])
        _hlautil.connect_window(
            self.centralwidget.pushButton_CV1, _PSDetailWindow, self,
            psname=corrs[2])
        self.centralwidget.PyDMLabel_KickRBCV1.channel = (
            self._prefix + corrs[2] + ':Kick-RB')

        self.centralwidget.pushButton_CV2.setText(corrs[3])
        _hlautil.connect_window(
            self.centralwidget.pushButton_CV2, _PSDetailWindow, self,
            psname=corrs[3])
        self.centralwidget.PyDMLabel_KickRBCV2.channel = (
            self._prefix + corrs[3] + ':Kick-RB')

    def _set_status_labels(self):
        for i in range(4):
            exec('self.centralwidget.label_status{0}.setText('
                 'Const.STATUSLABELS[{0}])'.format(i))


class CorrParamsDetailWindow(SiriusMainWindow):
    """Correction parameters detail window."""

    def __init__(self, tl, parent=None, prefix=None):
        """Class constructor."""
        super(CorrParamsDetailWindow, self).__init__(parent)
        self._tl = tl
        self.setObjectName(tl.upper()+'App')
        self._prefix = prefix
        self.setWindowTitle(self._tl +
                            ' Position and Angle Correction Parameters')
        self._setupUi()

    def _setupUi(self):
        label_configname = QLabel('<h4>Configuration Name</h4>', self,
                                  alignment=Qt.AlignCenter)
        self.pydmlinedit_configname = _ConfigLineEdit(
            parent=self,
            init_channel=self._prefix+self._tl+'-Glob:AP-PosAng:ConfigName-SP')
        self.pydmlabel_configname = PyDMLabel(
            parent=self,
            init_channel=self._prefix+self._tl+'-Glob:AP-PosAng:ConfigName-RB')

        label_matrix_X = QLabel('<h4>Matrix X</h4>', self,
                                alignment=Qt.AlignCenter)
        self.table_matrix_X = PyDMWaveformTable(
            parent=self,
            init_channel=self._prefix+self._tl+'-Glob:AP-PosAng:RespMatX-Mon')
        self.table_matrix_X.setObjectName('table_matrix_X')
        self.table_matrix_X.setStyleSheet("""
            #table_matrix_X{
                min-width:20.72em;
                min-height:4.65em; max-height:4.65em;}""")
        self.table_matrix_X.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_matrix_X.setRowCount(2)
        self.table_matrix_X.setColumnCount(2)
        self.table_matrix_X.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_matrix_X.horizontalHeader().setVisible(False)
        self.table_matrix_X.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_matrix_X.verticalHeader().setVisible(False)
        self.table_matrix_X.setSizePolicy(QSzPlcy.MinimumExpanding,
                                          QSzPlcy.Preferred)

        label_matrix_Y = QLabel('<h4>Matrix Y</h4>', self,
                                alignment=Qt.AlignCenter)
        self.table_matrix_Y = PyDMWaveformTable(
            parent=self,
            init_channel=self._prefix+self._tl+'-Glob:AP-PosAng:RespMatY-Mon')
        self.table_matrix_Y.setObjectName('table_matrix_Y')
        self.table_matrix_Y.setStyleSheet("""
            #table_matrix_Y{
                min-width:20.72em;
                min-height:4.65em; max-height:4.65em;}""")
        self.table_matrix_Y.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_matrix_Y.setRowCount(2)
        self.table_matrix_Y.setColumnCount(2)
        self.table_matrix_Y.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_matrix_Y.horizontalHeader().setVisible(False)
        self.table_matrix_Y.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_matrix_Y.verticalHeader().setVisible(False)
        self.table_matrix_Y.setSizePolicy(QSzPlcy.MinimumExpanding,
                                          QSzPlcy.Preferred)

        self.bt_apply = QPushButton('Ok', self)
        self.bt_apply.clicked.connect(self.close)

        lay = QGridLayout()
        lay.addItem(
            QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Expanding), 0, 1)
        lay.addWidget(label_configname, 1, 1, 1, 2)
        lay.addWidget(self.pydmlinedit_configname, 2, 1)
        lay.addWidget(self.pydmlabel_configname, 2, 2)
        lay.addItem(
            QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Expanding), 3, 1)
        lay.addWidget(label_matrix_X, 4, 1, 1, 2)
        lay.addWidget(self.table_matrix_X, 5, 1, 1, 2)
        lay.addItem(
            QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Expanding), 6, 1)
        lay.addWidget(label_matrix_Y, 7, 1, 1, 2)
        lay.addWidget(self.table_matrix_Y, 8, 1, 1, 2)
        lay.addItem(
            QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Expanding), 9, 1)
        lay.addWidget(self.bt_apply, 10, 2)
        self.centralwidget = QGroupBox('Correction Parameters')
        self.centralwidget.setLayout(lay)
        self.setCentralWidget(self.centralwidget)


class _ConfigLineEdit(PyDMLineEdit):

    def mouseReleaseEvent(self, ev):
        if 'TB' in self.channel:
            config_type = 'tb_posang_respm'
        elif 'TS' in self.channel:
            config_type = 'ts_posang_respm'
        popup = _LoadConfigDialog(config_type)
        popup.configname.connect(self._config_changed)
        popup.exec_()

    def _config_changed(self, configname):
        self.setText(configname)
        self.send_value()
        self.value_changed(configname)
