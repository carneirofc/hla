"""SiriusScrnView widget."""

import sys
import time
from threading import Thread
from qtpy.QtWidgets import QGridLayout, QHBoxLayout, QFormLayout, \
                           QSpacerItem, QWidget, QGroupBox, QLabel, \
                           QComboBox, QPushButton, QCheckBox, QMessageBox, \
                           QSizePolicy as QSzPlcy, QSpinBox
from qtpy.QtCore import Qt, Slot
from pydm.widgets import PyDMLabel, PyDMEnumComboBox
from siriuspy.envars import vaca_prefix as _vaca_prefix
from siriushla import util
from siriushla.widgets import PyDMLed, SiriusLedAlert
from siriushla.widgets.signal_channel import SiriusConnectionSignal
from siriushla.widgets.windows import SiriusMainWindow
from siriushla.as_di_scrns.base import \
    SiriusImageView as _SiriusImageView, \
    create_propty_layout as _create_propty_layout
from siriushla.as_di_scrns.scrn_details import \
    ScrnSettingsDetails as _ScrnSettingsDetails


class SiriusScrnView(QWidget):
    """
    Class to read Sirius screen cameras image data.

    To allow saving a grid correctly, control calibrationgrid_flag, which
    indicates if the screen is in calibration grid position.
    You can control it by using the method/Slot updateCalibrationGridFlag.
    """

    def __init__(self, parent=None, prefix=_vaca_prefix, device=None):
        """Initialize object."""
        QWidget.__init__(self, parent=parent)
        self.prefix = prefix
        self.device = device
        self.scrn_prefix = self.prefix+self.device
        self._calibrationgrid_flag = False
        screen_type_conn = SiriusConnectionSignal(
            self.scrn_prefix+':ScrnType-Sts')
        screen_type_conn.new_value_signal.connect(
            self.updateCalibrationGridFlag)
        self._setupUi()

    @property
    def calibrationgrid_flag(self):
        """Indicate if the screen device is in calibration grid position."""
        return self._calibrationgrid_flag

    @Slot(int)
    def updateCalibrationGridFlag(self, new_state):
        """Update calibrationgrid_flag property."""
        if new_state != self._calibrationgrid_flag:
            self._calibrationgrid_flag = new_state

            if new_state == 1:
                self.pushbutton_savegrid.setEnabled(True)
            else:
                self.pushbutton_savegrid.setEnabled(False)

    def _setupUi(self):
        self.setLayout(QGridLayout())

        self.cameraview_widget = QWidget()
        self.cameraview_widget.setLayout(self._cameraviewLayout())
        self.layout().addWidget(self.cameraview_widget, 0, 0, 1, 5)

        self.layout().addItem(
            QSpacerItem(4, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 1, 0)

        self.settings_groupBox = QGroupBox('Settings', self)
        self.settings_groupBox.setLayout(self._settingsLayout())
        self.layout().addWidget(self.settings_groupBox, 2, 1, 3, 1)

        self.layout().addItem(
            QSpacerItem(10, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 2, 2)

        self.statistics_groupBox = QGroupBox('Statistics', self)
        self.statistics_groupBox.setLayout(self._statisticsLayout())
        self.layout().addWidget(self.statistics_groupBox, 2, 3)
        self.statistics_groupBox.setSizePolicy(
            QSzPlcy.Expanding, QSzPlcy.Expanding)
        self.statistics_groupBox.setStyleSheet("""
            .QLabel{
                min-width:0.32em;\nmax-width:0.32em;\n
                min-height:1.29em;\nmax-height:1.29em;\n}
            QLabel{
                qproperty-alignment: AlignCenter;\n}
            PyDMWidget{
                min-width:4.84em;\nmax-width:4.84em;\n
                min-height:1.29em;\nmax-height:1.29em;\n}""")

        self.layout().addItem(
            QSpacerItem(30, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 3, 3)

        self.calibrationgrid_groupBox = QGroupBox('Calibration')
        self.calibrationgrid_groupBox.setLayout(self._calibrationgridLayout())
        self.calibrationgrid_groupBox.setSizePolicy(
            QSzPlcy.Expanding, QSzPlcy.Expanding)
        self.calibrationgrid_groupBox.layout().setAlignment(Qt.AlignHCenter)
        self.layout().addWidget(self.calibrationgrid_groupBox, 4, 3)

        self.layout().addItem(
            QSpacerItem(4, 20, QSzPlcy.Preferred, QSzPlcy.Preferred), 5, 4)

        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(1, 10)
        self.layout().setColumnStretch(2, 1)
        self.layout().setColumnStretch(3, 10)
        self.layout().setColumnStretch(4, 1)
        self.layout().setRowStretch(0, 34)
        self.layout().setRowStretch(1, 1)
        self.layout().setRowStretch(2, 13)
        self.layout().setRowStretch(3, 1)
        self.layout().setRowStretch(4, 13)
        self.layout().setRowStretch(5, 1)

    def _cameraviewLayout(self):
        label = QLabel(self.device, self)
        label.setStyleSheet("""font-weight: bold;max-height:1.29em;""")
        label.setAlignment(Qt.AlignCenter)
        self.image_view = _SiriusImageView(
            parent=self,
            image_channel=self.scrn_prefix+':ImgData-Mon',
            width_channel=self.scrn_prefix+':ImgROIWidth-RB',
            offsetx_channel=self.scrn_prefix+':ImgROIOffsetX-RB',
            offsety_channel=self.scrn_prefix+':ImgROIOffsetY-RB',
            maxwidth_channel=self.scrn_prefix+':ImgMaxWidth-Cte',
            maxheight_channel=self.scrn_prefix+':ImgMaxHeight-Cte')
        self.image_view.setObjectName('ScrnView')
        self.image_view.normalizeData = True
        self.image_view.readingOrder = self.image_view.Clike
        self.image_view.maxRedrawRate = 15
        self.image_view.setStyleSheet("""
            #ScrnView{min-width:42em; min-height:32em;}""")
        self.image_view.failToSaveGrid.connect(self._showFailToSaveGridMsg)

        lay = QGridLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(label, 0, 1)
        lay.addItem(QSpacerItem(40, 2, QSzPlcy.Preferred, QSzPlcy.Fixed), 1, 1)
        lay.addWidget(self.image_view, 2, 1)
        return lay

    def _calibrationgridLayout(self):
        self.checkBox_showgrid = QCheckBox('Show', self)
        self.checkBox_showgrid.setEnabled(False)
        self.checkBox_showgrid.setStyleSheet("""
            min-width:4.36em;\nmax-width:4.36em;\n
            min-height:1.29em;\nmax-height:1.29em;\n""")
        self.checkBox_showgrid.toggled.connect(
            self.image_view.showCalibrationGrid)
        self.pushbutton_savegrid = QPushButton('Save', self)
        self.pushbutton_savegrid.setEnabled(False)
        self.pushbutton_savegrid.setStyleSheet("""
            min-width:4.36em;\nmax-width:4.36em;\n
            min-height:1.29em;\nmax-height:1.29em;\n""")
        self.pushbutton_savegrid.clicked.connect(self._saveCalibrationGrid)
        hbox_grid = QHBoxLayout()
        hbox_grid.addWidget(self.checkBox_showgrid)
        hbox_grid.addWidget(self.pushbutton_savegrid)

        self.spinbox_gridfilterfactor = QSpinBox()
        self.spinbox_gridfilterfactor.setMaximum(100)
        self.spinbox_gridfilterfactor.setMinimum(0)
        self.spinbox_gridfilterfactor.setValue(
            self.image_view.calibration_grid_filterfactor)
        self.spinbox_gridfilterfactor.editingFinished.connect(
            self._setCalibrationGridFilterFactor)
        self.spinbox_gridfilterfactor.setStyleSheet("""
            min-width:2.90em;\nmax-width:2.90em;""")
        hbox_filter = QHBoxLayout()
        hbox_filter.setSpacing(0)
        hbox_filter.addWidget(QLabel('Show levels <'))
        hbox_filter.addWidget(self.spinbox_gridfilterfactor)
        hbox_filter.addWidget(QLabel('%'))

        hbox_EnblLED = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='EnblLED',
            propty_type='enbldisabl', width=4.68)

        lay = QFormLayout()
        lay.addItem(QSpacerItem(40, 10, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.addRow('     Grid: ', hbox_grid)
        lay.addItem(QSpacerItem(40, 10, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.addRow('     ', hbox_filter)
        lay.addItem(QSpacerItem(40, 20, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.addRow('     LED: ', hbox_EnblLED)
        lay.addItem(QSpacerItem(40, 10, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.setLabelAlignment(Qt.AlignRight)
        lay.setFormAlignment(Qt.AlignCenter)
        return lay

    def _settingsLayout(self):
        label_CamEnbl = QLabel('Enable: ', self, alignment=Qt.AlignCenter)
        hbox_CamEnbl = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='CamEnbl',
            propty_type='enbldisabl', width=4.68)

        label_CamAcqPeriod = QLabel('Acquire\nPeriod [s]:', self,
                                    alignment=Qt.AlignCenter)
        hbox_CamAcqPeriod = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='CamAcqPeriod',
            propty_type='sprb', width=4.68)

        label_CamExposureTime = QLabel('Exposure\nTime [us]:', self,
                                       alignment=Qt.AlignCenter)
        hbox_CamExposureTime = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='CamExposureTime',
            propty_type='sprb', width=4.68)

        label_CamGain = QLabel('Gain[dB]:', self, alignment=Qt.AlignRight)
        hbox_CamGain = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='CamGain',
            propty_type='sprb', width=4.68)
        hbox_AutoCamGain = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='AutoGain',
            propty_type='', width=4.68, cmd={'label': 'Auto Gain',
                                             'pressValue': 1,
                                             'name': 'CamAutoGain'})

        label_ROIOffsetX = QLabel('Offset X: ', self, alignment=Qt.AlignRight)
        hbox_ROIOffsetX = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='ImgROIOffsetX',
            propty_type='sprb', width=4.68)

        label_ROIOffsetY = QLabel('Offset Y: ', self, alignment=Qt.AlignRight)
        hbox_ROIOffsetY = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='ImgROIOffsetY',
            propty_type='sprb', width=4.68)

        label_ROIWidth = QLabel('Width: ', self, alignment=Qt.AlignRight)
        hbox_ROIWidth = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='ImgROIWidth',
            propty_type='sprb', width=4.68)

        label_ROIHeight = QLabel('Heigth: ', self, alignment=Qt.AlignRight)
        hbox_ROIHeight = _create_propty_layout(
            parent=self, prefix=self.scrn_prefix, propty='ImgROIHeight',
            propty_type='sprb', width=4.68)

        self.pb_moreSettings = QPushButton('More settings...', self)
        util.connect_window(self.pb_moreSettings, _ScrnSettingsDetails,
                            parent=self, prefix=self.prefix,
                            device=self.device)

        lay = QFormLayout()
        lay.setFormAlignment(Qt.AlignCenter)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.addRow(QLabel('<h4>Camera Acquisition</h4>',
                          alignment=Qt.AlignCenter))
        lay.addRow(label_CamEnbl, hbox_CamEnbl)
        lay.addRow(label_CamAcqPeriod, hbox_CamAcqPeriod)
        lay.addRow(label_CamExposureTime, hbox_CamExposureTime)
        lay.addRow(label_CamGain, hbox_CamGain)
        lay.addRow('', hbox_AutoCamGain)
        lay.addItem(QSpacerItem(4, 20, QSzPlcy.Fixed, QSzPlcy.Preferred))
        lay.addRow(QLabel('<h4>Camera ROI Settings [pixels]</h4>',
                          alignment=Qt.AlignCenter))
        lay.addRow(label_ROIWidth, hbox_ROIWidth)
        lay.addRow(label_ROIHeight, hbox_ROIHeight)
        lay.addRow(label_ROIOffsetX, hbox_ROIOffsetX)
        lay.addRow(label_ROIOffsetY, hbox_ROIOffsetY)
        lay.addItem(QSpacerItem(4, 20, QSzPlcy.Fixed, QSzPlcy.Preferred))
        lay.addRow('', self.pb_moreSettings)
        return lay

    def _statisticsLayout(self):
        # - Method
        label_Method = QLabel('CalcMethod: ', self)
        label_Method.setStyleSheet("""min-width:6em;""")

        self.comboBox_Method = QComboBox(self)
        self.comboBox_Method.addItem('DimFei', 0)
        self.comboBox_Method.addItem('NDStats', 1)
        self.comboBox_Method.setCurrentIndex(0)
        self.comboBox_Method.setStyleSheet("""
            QComboBox::item {\nheight: 1em;}
            QComboBox{\nmin-width: 6em;}
            """)
        self.comboBox_Method.currentIndexChanged.connect(
            self._handleShowStatistics)

        # - Centroid
        label_Centroid = QLabel('Centroid [mm]', self)
        label_Centroid.setStyleSheet("""min-width:15em;max-width:25em;""")
        label_i_Center = QLabel('(', self)

        self.PyDMLabel_CenterXDimFei = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':CenterXDimFei-Mon')
        self.PyDMLabel_CenterXNDStats = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':CenterXNDStats-Mon')
        self.PyDMLabel_CenterXNDStats.setVisible(False)

        label_m_Center = QLabel(',', self)

        self.PyDMLabel_CenterYDimFei = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':CenterYDimFei-Mon')
        self.PyDMLabel_CenterYNDStats = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':CenterYNDStats-Mon')
        self.PyDMLabel_CenterYNDStats.setVisible(False)

        label_f_Center = QLabel(')', self)

        # - Sigma
        label_Sigma = QLabel('Sigma [mm]', self)
        label_Sigma.setStyleSheet("""min-width:15em;max-width:25em;""")
        label_i_Sigma = QLabel('(', self)

        self.PyDMLabel_SigmaXDimFei = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':SigmaXDimFei-Mon')
        self.PyDMLabel_SigmaXNDStats = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':SigmaXNDStats-Mon')
        self.PyDMLabel_SigmaXNDStats.setVisible(False)

        label_m_Sigma = QLabel(',', self)

        self.PyDMLabel_SigmaYDimFei = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':SigmaYDimFei-Mon')
        self.PyDMLabel_SigmaYNDStats = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':SigmaYNDStats-Mon')
        self.PyDMLabel_SigmaYNDStats.setVisible(False)

        label_f_Sigma = QLabel(')', self)

        # - Theta
        label_Theta = QLabel('Theta [rad]')
        label_Theta.setStyleSheet("""min-width:15em;max-width:25em;""")
        label_i_Theta = QLabel('(', self)

        self.PyDMLabel_ThetaDimFei = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':ThetaDimFei-Mon')
        self.PyDMLabel_ThetaNDStats = PyDMLabel(
            parent=self, init_channel=self.scrn_prefix+':ThetaNDStats-Mon')
        self.PyDMLabel_ThetaNDStats.setVisible(False)

        label_f_Theta = QLabel(')', self)

        lay = QGridLayout()
        lay.addItem(QSpacerItem(20, 2, QSzPlcy.Fixed, QSzPlcy.Expanding), 0, 0)
        lay.addWidget(label_Method, 1, 1, 1, 2)
        lay.addWidget(self.comboBox_Method, 1, 4)
        lay.addItem(QSpacerItem(4, 2, QSzPlcy.Fixed, QSzPlcy.Preferred), 2, 2)
        lay.addWidget(label_Centroid, 3, 1, 1, 5)
        lay.addWidget(label_i_Center, 4, 1)
        lay.addWidget(self.PyDMLabel_CenterXDimFei, 4, 2)
        lay.addWidget(self.PyDMLabel_CenterXNDStats, 4, 2)
        lay.addWidget(label_m_Center, 4, 3)
        lay.addWidget(self.PyDMLabel_CenterYDimFei, 4, 4)
        lay.addWidget(self.PyDMLabel_CenterYNDStats, 4, 4)
        lay.addWidget(label_f_Center, 4, 5)
        lay.addItem(QSpacerItem(4, 2, QSzPlcy.Fixed, QSzPlcy.Preferred), 5, 2)
        lay.addWidget(label_Sigma, 6, 1, 1, 5)
        lay.addWidget(label_i_Sigma, 7, 1)
        lay.addWidget(self.PyDMLabel_SigmaXDimFei, 7, 2)
        lay.addWidget(self.PyDMLabel_SigmaXNDStats, 7, 2)
        lay.addWidget(label_m_Sigma, 7, 3)
        lay.addWidget(self.PyDMLabel_SigmaYDimFei, 7, 4)
        lay.addWidget(self.PyDMLabel_SigmaYNDStats, 7, 4)
        lay.addWidget(label_f_Sigma, 7, 5)
        lay.addItem(QSpacerItem(4, 2, QSzPlcy.Fixed, QSzPlcy.Preferred), 8, 2)
        lay.addWidget(label_Theta, 9, 1, 1, 5)
        lay.addWidget(label_i_Theta, 10, 1)
        lay.addWidget(self.PyDMLabel_ThetaDimFei, 10, 2, 1, 3)
        lay.addWidget(self.PyDMLabel_ThetaNDStats, 10, 2, 1, 3)
        lay.addWidget(label_f_Theta, 10, 5)
        lay.addItem(
            QSpacerItem(20, 2, QSzPlcy.Fixed, QSzPlcy.Expanding), 11, 6)
        return lay

    def _handleShowStatistics(self, visible):
        self.PyDMLabel_CenterXDimFei.setVisible(not visible)
        self.PyDMLabel_CenterXNDStats.setVisible(visible)
        self.PyDMLabel_CenterYDimFei.setVisible(not visible)
        self.PyDMLabel_CenterYNDStats.setVisible(visible)
        self.PyDMLabel_ThetaDimFei.setVisible(not visible)
        self.PyDMLabel_ThetaNDStats.setVisible(visible)
        self.PyDMLabel_SigmaXDimFei.setVisible(not visible)
        self.PyDMLabel_SigmaXNDStats.setVisible(visible)
        self.PyDMLabel_SigmaYDimFei.setVisible(not visible)
        self.PyDMLabel_SigmaYNDStats.setVisible(visible)

    def _saveCalibrationGrid(self):
        Thread(target=self._saveCalibrationGrid_thread, daemon=True).start()

    def _saveCalibrationGrid_thread(self):
        roi_h = float(self.PyDMLabel_ImgROIHeight.text())
        roi_w = float(self.PyDMLabel_ImgROIWidth.text())
        roi_offsetx = float(self.PyDMLabel_ImgROIOffsetX.text())
        roi_offsety = float(self.PyDMLabel_ImgROIOffsetY.text())

        # Change ROI to get entire image
        self.PyDMStateButton_CamEnbl.send_value_signal[int].emit(0)
        self.PyDMSpinbox_ImgROIHeight.send_value_signal[float].emit(
            float(self.image_view.image_maxheight))
        self.PyDMSpinbox_ImgROIWidth.send_value_signal[float].emit(
            float(self.image_view.image_maxwidth))
        self.PyDMSpinbox_ImgROIOffsetX.send_value_signal[float].emit(0)
        self.PyDMSpinbox_ImgROIOffsetY.send_value_signal[float].emit(0)
        self.PyDMStateButton_CamEnbl.send_value_signal[int].emit(1)

        # Save grid
        self.image_view.saveCalibrationGrid()

        # Change ROI to original size
        self.PyDMStateButton_CamEnbl.send_value_signal[int].emit(0)
        self.PyDMSpinbox_ImgROIHeight.send_value_signal[float].emit(roi_h)
        self.PyDMSpinbox_ImgROIWidth.send_value_signal[float].emit(roi_w)
        self.PyDMSpinbox_ImgROIOffsetX.send_value_signal[float].emit(
            roi_offsetx)
        self.PyDMSpinbox_ImgROIOffsetY.send_value_signal[float].emit(
            roi_offsety)
        self.PyDMStateButton_CamEnbl.send_value_signal[int].emit(1)

        # Enable showing saved grid
        time.sleep(0.1)
        self.checkBox_showgrid.setEnabled(True)

    def _setCalibrationGridFilterFactor(self):
        self.image_view.set_calibration_grid_filterfactor(
            self.spinbox_gridfilterfactor.value())

    @Slot()
    def _showFailToSaveGridMsg(self):
        QMessageBox.warning(self, 'Warning',
                            'Could not save calibration grid!',
                            QMessageBox.Ok)


if __name__ == '__main__':
    """Run test."""
    import os
    from siriushla.sirius_application import SiriusApplication

    os.environ['EPICS_CA_MAX_ARRAY_BYTES'] = '200000000'
    app = SiriusApplication()

    centralwidget = QWidget()
    prefix = _vaca_prefix
    scrn_device = 'TB-01:DI-Scrn-1'
    cw = QWidget()
    scrn_view = SiriusScrnView(prefix=prefix, device=scrn_device)
    cb_scrntype = PyDMEnumComboBox(
        parent=cw, init_channel=prefix+scrn_device+':ScrnType-Sel')
    l_scrntype = PyDMLabel(
        parent=cw, init_channel=prefix+scrn_device+':ScrnType-Sts')
    led_scrntype = SiriusLedAlert(
        parent=cw, init_channel=prefix+scrn_device+':ScrnType-Sts')
    led_scrntype.shape = 2
    led_scrntype.setStyleSheet("""min-height:1.29em; max-height:1.29em;""")
    led_movests = PyDMLed(
        parent=cw, init_channel=prefix+scrn_device+':DoneMov-Mon',
        color_list=[PyDMLed.LightGreen, PyDMLed.DarkGreen])
    led_movests.shape = 2
    led_movests.setStyleSheet("""min-height:1.29em; max-height:1.29em;""")

    lay = QGridLayout()
    lay.addWidget(QLabel('<h3>Screen View</h3>',
                         cw, alignment=Qt.AlignCenter), 0, 0, 1, 2)
    lay.addItem(QSpacerItem(20, 20, QSzPlcy.Fixed, QSzPlcy.Fixed), 1, 0)
    lay.addWidget(QLabel('Select Screen Type: ', cw,
                         alignment=Qt.AlignRight), 2, 0)
    lay.addWidget(cb_scrntype, 2, 1)
    lay.addWidget(l_scrntype, 2, 2)
    lay.addWidget(led_scrntype, 2, 3)
    lay.addWidget(QLabel('Motor movement status: ', cw,
                         alignment=Qt.AlignRight), 3, 0)
    lay.addWidget(led_movests, 3, 1)

    lay.addItem(QSpacerItem(20, 40, QSzPlcy.Fixed, QSzPlcy.Fixed), 4, 0)
    lay.addWidget(scrn_view, 5, 0, 1, 4)
    cw.setLayout(lay)

    window = SiriusMainWindow()
    window.setWindowTitle('Screen View: '+scrn_device)
    window.setCentralWidget(cw)
    window.show()
    sys.exit(app.exec_())