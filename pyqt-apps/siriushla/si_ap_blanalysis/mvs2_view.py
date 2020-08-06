"""Beam Line MVS2 View."""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, \
    QFormLayout
import qtawesome as qta
from pydm.widgets import PyDMLabel

from siriuspy.envars import VACA_PREFIX
from siriuspy.namesys import SiriusPVName

from siriushla.util import get_appropriate_color
from siriushla.widgets import SiriusMainWindow, SiriusProcessImage, \
    SiriusSpinbox, PyDMStateButton, SiriusLabel, SiriusLedState


class BeamLineMVS2View(SiriusMainWindow):
    """Beam line MVS2 View."""

    def __init__(self, parent=None, prefix=VACA_PREFIX,
                 device_analysis='', device_cam=''):
        super().__init__(parent)
        self._prefix = prefix
        self._device_analysis = SiriusPVName(device_analysis[:-1])
        self._device_cam = device_cam[:-1]
        self._color = get_appropriate_color('ID')
        self._title = self._device_analysis.dev + ' MVS2 Analysis Window'
        self.setWindowTitle(self._title)
        self.setWindowIcon(qta.icon('mdi.camera-control', color=self._color))
        self.setObjectName('IDApp')
        self._setupUi()

    def _setupUi(self):
        label = QLabel('<h3>'+self._title+'</h3>', self,
                       alignment=Qt.AlignCenter)

        self._process_image = SiriusProcessImage(
            self, device=self._device_analysis, orientation='H',
            convertion_set=False)
        self._process_image.image_view.colorMapMax = 2**16-1

        # IOC control
        gbox_ctrl = QGroupBox('Analysis Control')
        lay_ctrl = QGridLayout(gbox_ctrl)

        self._ld_enbl = QLabel('Start/Stop Acq.: ')
        self._sb_enbl = PyDMStateButton(
            gbox_ctrl, self._device_analysis+':MeasureCtrl-Sel')
        self._lb_enbl = PyDMLabel(
            gbox_ctrl, self._device_analysis+':MeasureCtrl-Sts')

        self._ld_rate = QLabel('Acq. Rate: ')
        self._sb_rate = SiriusSpinbox(
            gbox_ctrl, self._device_analysis+':MeasureRate-SP')
        self._sb_rate.showStepExponent = False
        self._lb_rate = PyDMLabel(
            gbox_ctrl, self._device_analysis+':MeasureRate-RB')

        self._ld_tgtx = QLabel('Target X: ')
        self._sb_tgtx = SiriusSpinbox(
            gbox_ctrl, self._device_analysis+':TargetPosX-SP')
        self._sb_tgtx.showStepExponent = False
        self._lb_tgtx = PyDMLabel(
            gbox_ctrl, self._device_analysis+':TargetPosX-RB')

        self._ld_tgty = QLabel('Target Y: ')
        self._sb_tgty = SiriusSpinbox(
            gbox_ctrl, self._device_analysis+':TargetPosY-SP')
        self._sb_tgty.showStepExponent = False
        self._lb_tgty = PyDMLabel(
            gbox_ctrl, self._device_analysis+':TargetPosY-RB')

        lay_ctrl.setAlignment(Qt.AlignTop)
        lay_ctrl.addWidget(self._ld_enbl, 0, 0, 2, 1)
        lay_ctrl.addWidget(self._sb_enbl, 0, 1)
        lay_ctrl.addWidget(self._lb_enbl, 1, 1)
        lay_ctrl.addWidget(self._ld_rate, 2, 0, 2, 1)
        lay_ctrl.addWidget(self._sb_rate, 2, 1)
        lay_ctrl.addWidget(self._lb_rate, 3, 1)
        lay_ctrl.addWidget(self._ld_tgtx, 4, 0, 2, 1)
        lay_ctrl.addWidget(self._sb_tgtx, 4, 1)
        lay_ctrl.addWidget(self._lb_tgtx, 5, 1)
        lay_ctrl.addWidget(self._ld_tgty, 6, 0, 2, 1)
        lay_ctrl.addWidget(self._sb_tgty, 6, 1)
        lay_ctrl.addWidget(self._lb_tgty, 7, 1)

        gbox_sofb = QGroupBox('SOFB Bump')
        lay_sofb = QGridLayout(gbox_sofb)

        self._ld_bmpx = QLabel('Ang. X: ')
        self._lb_bmpx = SiriusLabel(
            gbox_sofb, self._device_analysis+':SOFBBumpX-Mon')
        self._ld_bmpy = QLabel('Ang. Y: ')
        self._lb_bmpy = SiriusLabel(
            gbox_sofb, self._device_analysis+':SOFBBumpY-Mon')
        self._lb_bmpx.showUnits = True
        self._lb_bmpy.showUnits = True

        lay_sofb.setAlignment(Qt.AlignTop)
        lay_sofb.addWidget(self._ld_bmpx, 0, 0, 2, 1)
        lay_sofb.addWidget(self._lb_bmpx, 0, 1)
        lay_sofb.addWidget(self._ld_bmpy, 1, 0, 2, 1)
        lay_sofb.addWidget(self._lb_bmpy, 1, 1)

        # Camera Acquisition Status
        gbox_acqsett = QGroupBox('Camera Acquisition Statuses')
        lay_acqsett = QGridLayout(gbox_acqsett)

        self._ld_acqtime = QLabel('Acquire Time: ')
        self._sb_acqtime = SiriusSpinbox(
            gbox_ctrl, self._device_cam + ':cam1:AcquireTime')
        self._sb_acqtime.showStepExponent = False
        self._lb_acqtime = PyDMLabel(
            gbox_acqsett, self._device_cam+':cam1:AcquireTime_RBV')
        self._lb_acqtime.showUnits = True

        self._ld_acqperd = QLabel('Acquire Period: ')
        self._sb_acqperd = SiriusSpinbox(
            gbox_ctrl, self._device_cam + ':cam1:AcquirePeriod')
        self._sb_acqperd.showStepExponent = False
        self._lb_acqperd = PyDMLabel(
            gbox_acqsett, self._device_cam+':cam1:AcquirePeriod_RBV')
        self._lb_acqperd.showUnits = True

        self._ld_numimgs = QLabel('# Images: ')
        self._lb_numimgs = PyDMLabel(
            gbox_acqsett, self._device_cam+':cam1:NumImages_RBV')

        self._ld_imgmode = QLabel('Image Mode: ')
        self._lb_imgmode = PyDMLabel(
            gbox_acqsett, self._device_cam+':cam1:ImageMode_RBV')

        self._ld_acqsts = QLabel('Acquire Status: ')
        self._pb_acqsts = PyDMStateButton(
            gbox_acqsett, self._device_cam+':cam1:Acquire')
        self._lb_acqsts = SiriusLedState(
            gbox_acqsett, self._device_cam+':cam1:Acquire_RBV')

        self._ld_capsts = QLabel('Capture Status: ')
        self._pb_capsts = PyDMStateButton(
            gbox_acqsett, self._device_cam+':HDF1:Capture')
        self._lb_capsts = SiriusLedState(
            gbox_acqsett, self._device_cam+':HDF1:Capture_RBV')

        lay_acqsett.addWidget(self._ld_acqtime, 0, 0, 2, 1)
        lay_acqsett.addWidget(self._sb_acqtime, 0, 1)
        lay_acqsett.addWidget(self._lb_acqtime, 1, 1)
        lay_acqsett.addWidget(self._ld_acqperd, 2, 0, 2, 1)
        lay_acqsett.addWidget(self._sb_acqperd, 2, 1)
        lay_acqsett.addWidget(self._lb_acqperd, 3, 1)
        lay_acqsett.addWidget(self._ld_acqsts, 4, 0, 2, 1)
        lay_acqsett.addWidget(self._pb_acqsts, 4, 1)
        lay_acqsett.addWidget(self._lb_acqsts, 5, 1)
        lay_acqsett.addWidget(self._ld_capsts, 6, 0, 2, 1)
        lay_acqsett.addWidget(self._pb_capsts, 6, 1)
        lay_acqsett.addWidget(self._lb_capsts, 7, 1)
        lay_acqsett.addWidget(self._ld_numimgs, 8, 0)
        lay_acqsett.addWidget(self._lb_numimgs, 8, 1)
        lay_acqsett.addWidget(self._ld_imgmode, 9, 0)
        lay_acqsett.addWidget(self._lb_imgmode, 9, 1)

        self.cw = QWidget()
        self.cw.setStyleSheet('PyDMLabel{qproperty-alignment: AlignCenter;}')
        lay = QGridLayout(self.cw)
        lay.addWidget(label, 0, 0, 1, 2)
        lay.addWidget(self._process_image, 1, 0, 3, 1)
        lay.addWidget(gbox_ctrl, 1, 1)
        lay.addWidget(gbox_sofb, 2, 1)
        lay.addWidget(gbox_acqsett, 3, 1)
        lay.setColumnStretch(0, 7)
        lay.setColumnStretch(1, 2)
        self.setCentralWidget(self.cw)
