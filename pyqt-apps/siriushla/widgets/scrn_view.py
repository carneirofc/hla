"""SiriusScrnView widget."""

import numpy as np
import time
from threading import Thread
from pydm.PyQt.QtGui import (QGridLayout, QHBoxLayout, QFormLayout,
                             QSpacerItem, QWidget, QGroupBox, QLabel,
                             QComboBox, QPushButton, QCheckBox, QMessageBox)
from pydm.PyQt.QtGui import QSizePolicy as QSzPlcy
from pydm.PyQt.QtCore import Qt, pyqtSlot, pyqtSignal, pyqtProperty
from pydm.widgets import (PyDMImageView, PyDMLabel, PyDMSpinbox,
                          PyDMPushButton, PyDMEnumComboBox)
from pydm.widgets.channel import PyDMChannel
from siriuspy.envars import vaca_prefix as _vaca_prefix
from siriushla.widgets import PyDMStateButton, SiriusLedState
from siriushla.widgets.windows import SiriusMainWindow
from siriushla import util


class _SiriusImageView(PyDMImageView):
    """A PyDMImageView with methods to handle screens calibration grids."""

    failToSaveGrid = pyqtSignal()

    def __init__(self, parent=None,
                 image_channel=None, width_channel=None,
                 offsetx_channel=None, offsety_channel=None,
                 maxwidth_channel=None, maxheight_channel=None):
        """Initialize the object."""
        PyDMImageView.__init__(self, parent=parent,
                               image_channel=image_channel,
                               width_channel=width_channel)
        self._calibration_grid_image = None
        self._calibration_grid_maxdata = None
        self._calibration_grid_width = None
        self._image_roi_offsetx = 0
        self._offsetxchannel = offsetx_channel
        self._image_roi_offsety = 0
        self._offsetychannel = offsety_channel
        self._image_maxwidth = 0
        self._maxwidthchannel = maxwidth_channel
        self._image_maxheight = 0
        self._maxheightchannel = maxheight_channel
        self._show_calibration_grid = False

    @pyqtSlot()
    def saveCalibrationGrid(self):
        """Save current image as calibration_grid_image."""
        for i in range(40):
            if self.image_waveform.size == (
                    self.image_maxwidth*self.image_maxheight):
                img = self.image_waveform.copy()
                self._calibration_grid_width = self.imageWidth
                self._calibration_grid_maxdata = img.max()
                grid = np.where(img < 0.5*self._calibration_grid_maxdata,
                                True, False)
                if self.readingOrder == self.ReadingOrder.Clike:
                    self._calibration_grid_image = grid.reshape(
                        (-1, self._calibration_grid_width), order='C')
                else:
                    self._calibration_grid_image = grid.reshape(
                        (self._calibration_grid_width, -1), order='F')
                break
            time.sleep(0.05)
        else:
            self.failToSaveGrid.emit()

    @pyqtSlot(bool)
    def showCalibrationGrid(self, show):
        """Show calibration_grid_image over the current image_waveform."""
        self._show_calibration_grid = show

    def redrawImage(self):
        """
        Set the image data into the ImageItem, if needed.

        If necessary, reshape the image to 2D first.
        """
        if not self.needs_redraw:
            return
        image_dimensions = len(self.image_waveform.shape)
        img = np.array([])
        if image_dimensions == 1:
            if self.imageWidth < 1:
                # We don't have a width for this image yet, so we can't draw it
                return
            try:
                if self.readingOrder == self.ReadingOrder.Clike:
                    img = self.image_waveform.reshape((-1, self.imageWidth),
                                                      order='C')
                else:
                    img = self.image_waveform.reshape((self.imageWidth, -1),
                                                      order='F')
            except Exception:
                print('ImageWidth property does not match image dimentions!')
        else:
            img = self.image_waveform

        if len(img) <= 0:
            return
        if ((self._show_calibration_grid) and
                (self._calibration_grid_image is not None)):
            try:
                grid = self._adjust_calibration_grid(img)
                img[grid] = self._calibration_grid_maxdata
            except Exception:
                print('Grid dimentions do not match image dimentions!')
        if self._normalize_data:
            mini = self.image_waveform.min()
            maxi = self.image_waveform.max()
        else:
            mini = self.cm_min
            maxi = self.cm_max
        self.getImageItem().setLevels([mini, maxi])
        self.getImageItem().setImage(
            img,
            autoLevels=False,
            autoDownsample=True)
        self.needs_redraw = False

    def _adjust_calibration_grid(self, img):
        height = np.size(img, 0)
        width = np.size(img, 1)
        grid = self._calibration_grid_image[
            self._image_roi_offsety:(self._image_roi_offsety+height),
            self._image_roi_offsetx:(self._image_roi_offsetx+width)]
        return grid

    def roioffsetx_connection_state_changed(self, conn):
        """
        Callback invoked when the ROIOffsetX Channel connection state changes.

        Parameters
        ----------
        conn : bool
            The new connection state.
        """
        if not conn:
            self._image_roi_offsetx = 0

    def roioffsety_connection_state_changed(self, conn):
        """
        Callback invoked when the ROIOffsetY Channel connection state changes.

        Parameters
        ----------
        conn : bool
            The new connection state.
        """
        if not conn:
            self._image_roi_offsety = 0

    def image_roioffsetx_changed(self, new_offset):
        """
        Callback invoked when the ROIOffsetX Channel value changes.

        Parameters
        ----------
        new_offsetx : int
            The new image ROI horizontal offset
        """
        if new_offset is None:
            return
        self._image_roi_offsetx = new_offset

    def image_roioffsety_changed(self, new_offset):
        """
        Callback invoked when the ROIOffsetY Channel value changes.

        Parameters
        ----------
        new_offsety : int
            The new image ROI vertical offset
        """
        if new_offset is None:
            return
        self._image_roi_offsety = new_offset

    @property
    def image_maxwidth(self):
        return self._image_maxwidth

    def image_maxwidth_changed(self, new_max):
        """
        Callback invoked when the maxWidth Channel value changes.

        Parameters
        ----------
        new_max : int
            The new image max width
        """
        if new_max is None:
            return
        self._image_maxwidth = new_max

    @property
    def image_maxheight(self):
        return self._image_maxheight

    def image_maxheight_changed(self, new_max):
        """
        Callback invoked when the maxHeight Channel value changes.

        Parameters
        ----------
        new_max : int
            The new image max height
        """
        if new_max is None:
            return
        self._image_maxheight = new_max

    @pyqtProperty(str)
    def ROIOffsetXChannel(self):
        """
        The channel address in use for the image ROI horizontal offset.

        Returns
        -------
        str
            Channel address
        """
        return str(self._offsetxchannel)

    @ROIOffsetXChannel.setter
    def ROIOffsetXChannel(self, value):
        """
        The channel address in use for the image ROI horizontal offset.

        Parameters
        ----------
        value : str
            Channel address
        """
        if self._offsetxchannel != value:
            self._offsetxchannel = str(value)

    @pyqtProperty(str)
    def ROIOffsetYChannel(self):
        """
        The channel address in use for the image ROI vertical offset.

        Returns
        -------
        str
            Channel address
        """
        return str(self._offsetychannel)

    @ROIOffsetYChannel.setter
    def ROIOffsetYChannel(self, value):
        """
        The channel address in use for the image ROI vertical offset.

        Parameters
        ----------
        value : str
            Channel address
        """
        if self._offsetychannel != value:
            self._offsetychannel = str(value)

    @pyqtProperty(str)
    def maxWidthChannel(self):
        """
        The channel address in use for the image ROI horizontal offset.

        Returns
        -------
        str
            Channel address
        """
        return str(self._maxwidthchannel)

    @maxWidthChannel.setter
    def maxWidthChannel(self, value):
        """
        The channel address in use for the image ROI horizontal offset.

        Parameters
        ----------
        value : str
            Channel address
        """
        if self._maxwidthchannel != value:
            self._maxwidthchannel = str(value)

    @pyqtProperty(str)
    def maxHeightChannel(self):
        """
        The channel address in use for the image ROI vertical offset.

        Returns
        -------
        str
            Channel address
        """
        return str(self._maxheightchannel)

    @maxHeightChannel.setter
    def maxHeightChannel(self, value):
        """
        The channel address in use for the image ROI vertical offset.

        Parameters
        ----------
        value : str
            Channel address
        """
        if self._maxheightchannel != value:
            self._maxheightchannel = str(value)

    def channels(self):
        """
        Return the channels being used for this Widget.

        Returns
        -------
        channels : list
            List of PyDMChannel objects
        """
        if self._channels is None:
            self._channels = [
                PyDMChannel(
                    address=self.imageChannel,
                    connection_slot=self.image_connection_state_changed,
                    value_slot=self.image_value_changed,
                    severity_slot=self.alarmSeverityChanged),
                PyDMChannel(
                    address=self.widthChannel,
                    connection_slot=self.connectionStateChanged,
                    value_slot=self.image_width_changed,
                    severity_slot=self.alarmSeverityChanged),
                PyDMChannel(
                    address=self.ROIOffsetXChannel,
                    connection_slot=self.roioffsetx_connection_state_changed,
                    value_slot=self.image_roioffsetx_changed,
                    severity_slot=self.alarmSeverityChanged),
                PyDMChannel(
                    address=self.ROIOffsetYChannel,
                    connection_slot=self.roioffsety_connection_state_changed,
                    value_slot=self.image_roioffsety_changed,
                    severity_slot=self.alarmSeverityChanged),
                PyDMChannel(
                    address=self.maxWidthChannel,
                    value_slot=self.image_maxwidth_changed,
                    severity_slot=self.alarmSeverityChanged),
                PyDMChannel(
                    address=self.maxHeightChannel,
                    value_slot=self.image_maxheight_changed,
                    severity_slot=self.alarmSeverityChanged)]
        return self._channels


class SiriusScrnView(QWidget):
    """
    Class to read Sirius screen cameras image data.

    To allow saving a grid correctly, control calibrationgrid_flag, which
    indicates if the screen is in calibration grid position.
    You can control it by using the method/pyqtSlot updateCalibrationGridFlag.
    """

    def __init__(self, parent=None, prefix='', device=None):
        """Initialize object."""
        QWidget.__init__(self, parent=parent)
        if prefix == '':
            self.prefix = _vaca_prefix
        else:
            self.prefix = prefix
        self.device = device
        self._calibrationgrid_flag = False
        self.setLayout(QGridLayout())
        self.setStyleSheet("""font-size:20pt;""")
        self._setupUi()
        util.connect_window(self.pushbutton_openCameraSettingsDetails,
                            _CameraSettingsDetails, parent=self,
                            prefix=self.prefix, device=self.device)

    @property
    def calibrationgrid_flag(self):
        """Indicate if the screen device is in calibration grid position."""
        return self._calibrationgrid_flag

    @pyqtSlot(int)
    def updateCalibrationGridFlag(self, new_state):
        """Update calibrationgrid_flag property."""
        if new_state != self._calibrationgrid_flag:
            self._calibrationgrid_flag = new_state

            if new_state == 1:
                self.pushbutton_savegrid.setEnabled(True)
            else:
                self.pushbutton_savegrid.setEnabled(False)

    def _setupUi(self):
        self.cameraview_widget = QWidget()
        self.cameraview_widget.setLayout(self._cameraviewLayout())
        self.layout().addWidget(self.cameraview_widget, 1, 1, 1, 3)

        container = QWidget()
        layout_container = QHBoxLayout()
        self.calibrationgrid_widget = QWidget()
        self.calibrationgrid_widget.setLayout(self._calibrationgridLayout())
        self.calibrationgrid_widget.layout().setAlignment(Qt.AlignHCenter)
        self.imagesettings_widget = QWidget()
        self.imagesettings_widget.setLayout(self._imagesettingsLayout())
        layout_container.addWidget(self.calibrationgrid_widget)
        layout_container.setStretch(1, 2)
        layout_container.addWidget(self.imagesettings_widget)
        layout_container.setStretch(2, 1)
        container.setLayout(layout_container)
        self.layout().addWidget(container, 2, 1, 1, 3)

        self.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 3, 1)

        self.camerasettings_groupBox = QGroupBox('Camera Settings', self)
        self.camerasettings_groupBox.setLayout(self._camerasettingsLayout())
        self.layout().addWidget(self.camerasettings_groupBox, 4, 1)

        self.layout().addItem(
            QSpacerItem(60, 20, QSzPlcy.Fixed, QSzPlcy.Minimum), 4, 2)

        self.statistics_groupBox = QGroupBox('Statistics', self)
        self.statistics_groupBox.setLayout(self._statisticsLayout())
        self.layout().addWidget(self.statistics_groupBox, 4, 3)

        self.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 5, 1)

    def _cameraviewLayout(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(self.device, self)
        label.setStyleSheet("""font-weight: bold;""")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 0, 1)
        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 1, 1)
        self.image_view = _SiriusImageView(
            parent=self,
            image_channel='ca://'+self.prefix+self.device+':ImgData-Mon',
            width_channel='ca://'+self.prefix+self.device+':ImgROIWidth-RB',
            offsetx_channel='ca://'+self.prefix+self.device +
                            ':ImgROIOffsetX-RB',
            offsety_channel='ca://'+self.prefix+self.device +
                            ':ImgROIOffsetY-RB',
            maxwidth_channel='ca://'+self.prefix+self.device +
                            ':ImgMaxWidth-Mon',
            maxheight_channel='ca://'+self.prefix+self.device +
                            ':ImgMaxHeight-Mon')
        self.image_view.normalizeData = True
        self.image_view.readingOrder = self.image_view.Clike
        self.image_view.maxRedrawRate = 15
        self.image_view.setMinimumSize(920, 736)
        self.image_view.failToSaveGrid.connect(self._showFailToSaveGridMsg)
        layout.addWidget(self.image_view, 2, 1)
        return layout

    def _calibrationgridLayout(self):
        layout = QHBoxLayout()
        self.checkBox_showgrid = QCheckBox('Show grid', self)
        self.checkBox_showgrid.toggled.connect(
            self.image_view.showCalibrationGrid)
        layout.addWidget(self.checkBox_showgrid)
        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))
        self.pushbutton_savegrid = QPushButton('Save grid', self)
        self.pushbutton_savegrid.setEnabled(False)
        self.pushbutton_savegrid.setMinimumHeight(40)
        self.pushbutton_savegrid.clicked.connect(self._saveCalibrationGrid)
        layout.addWidget(self.pushbutton_savegrid)
        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))
        self.label = QLabel('Led: ', self)
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        self.PyDMStateButton_LedEnbl = PyDMStateButton(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':LedEnbl-Sel')
        self.PyDMStateButton_LedEnbl.shape = 1
        self.PyDMStateButton_LedEnbl.setMaximumHeight(40)
        self.PyDMStateButton_LedEnbl.setSizePolicy(
            QSzPlcy.Fixed, QSzPlcy.Maximum)
        layout.addWidget(self.PyDMStateButton_LedEnbl)
        self.SiriusLedState_LedEnbl = SiriusLedState(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':LedEnbl-Sts')
        self.SiriusLedState_LedEnbl.setMinimumSize(40, 40)
        self.SiriusLedState_LedEnbl.setMaximumHeight(40)
        self.SiriusLedState_LedEnbl.setSizePolicy(
            QSzPlcy.Minimum, QSzPlcy.Maximum)
        layout.addWidget(self.SiriusLedState_LedEnbl)
        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))
        layout.setAlignment(Qt.AlignVCenter)
        return layout

    def _imagesettingsLayout(self):
        layout = QGridLayout()
        self.label = QLabel('Zoom: ', self)
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label, 1, 1)
        self.pushButton_zoomOut = QPushButton('-', parent=self)
        self.pushButton_zoomOut.clicked.connect(self._zoomOut)
        self.pushButton_zoomOut.setMinimumSize(40, 40)
        self.pushButton_zoomOut.setMaximumSize(40, 40)
        layout.addWidget(self.pushButton_zoomOut, 1, 2)
        self.pushButton_zoomActualSize = QPushButton('100%', parent=self)
        self.pushButton_zoomActualSize.clicked.connect(
            self._zoomToActualSize)
        self.pushButton_zoomActualSize.setMinimumSize(80, 40)
        self.pushButton_zoomActualSize.setMaximumSize(80, 40)
        layout.addWidget(self.pushButton_zoomActualSize, 1, 3)
        self.pushButton_zoomIn = QPushButton('+', parent=self)
        self.pushButton_zoomIn.clicked.connect(self._zoomIn)
        self.pushButton_zoomIn.setMinimumSize(40, 40)
        self.pushButton_zoomIn.setMaximumSize(40, 40)
        layout.addWidget(self.pushButton_zoomIn, 1, 4)
        return layout

    def _camerasettingsLayout(self):
        layout = QGridLayout()
        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 2, 1)

        self.label = QLabel('Gain', self)
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label, 3, 1, 1, 2)
        self.PyDMSpinbox_CamGain = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamGain-SP')
        self.PyDMSpinbox_CamGain.setMaximumSize(220, 40)
        self.PyDMSpinbox_CamGain.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_CamGain.showStepExponent = False
        layout.addWidget(self.PyDMSpinbox_CamGain, 4, 1)
        self.PyDMLabel_CamGain = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamGain-RB')
        self.PyDMLabel_CamGain.setMaximumSize(220, 40)
        self.PyDMLabel_CamGain.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.PyDMLabel_CamGain, 4, 2)

        self.label = QLabel('Exposure Time', self)
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label, 5, 1, 1, 2)
        self.PyDMSpinbox_CamExposureTime = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamExposureTime-SP')
        self.PyDMSpinbox_CamExposureTime.setMaximumSize(220, 40)
        self.PyDMSpinbox_CamExposureTime.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_CamExposureTime.showStepExponent = False
        layout.addWidget(self.PyDMSpinbox_CamExposureTime, 6, 1)
        self.PyDMLabel_CamExposureTime = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamExposureTime-RB')
        self.PyDMLabel_CamExposureTime.setMaximumSize(220, 40)
        self.PyDMLabel_CamExposureTime.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.PyDMLabel_CamExposureTime, 6, 2)

        self.label = QLabel('ROI Offset X', self)
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label, 7, 1, 1, 2)
        self.PyDMSpinbox_ROIOffsetX = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetX-SP')
        self.PyDMSpinbox_ROIOffsetX.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIOffsetX.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIOffsetX.showStepExponent = False
        layout.addWidget(self.PyDMSpinbox_ROIOffsetX, 8, 1)
        self.PyDMLabel_ROIOffsetX = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetX-RB')
        self.PyDMLabel_ROIOffsetX.setMaximumSize(220, 40)
        self.PyDMLabel_ROIOffsetX.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.PyDMLabel_ROIOffsetX, 8, 2)

        self.label = QLabel('ROI Offset Y', self)
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label, 9, 1, 1, 2)
        self.PyDMSpinbox_ROIOffsetY = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetY-SP')
        self.PyDMSpinbox_ROIOffsetY.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIOffsetY.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIOffsetY.showStepExponent = False
        layout.addWidget(self.PyDMSpinbox_ROIOffsetY, 10, 1)
        self.PyDMLabel_ROIOffsetY = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetY-RB')
        self.PyDMLabel_ROIOffsetY.setMaximumSize(220, 40)
        self.PyDMLabel_ROIOffsetY.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.PyDMLabel_ROIOffsetY, 10, 2)

        self.label = QLabel('ROI Width', self)
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label, 11, 1, 1, 2)
        self.PyDMSpinbox_ROIWidth = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIWidth-SP')
        self.PyDMSpinbox_ROIWidth.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIWidth.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIWidth.showStepExponent = False
        layout.addWidget(self.PyDMSpinbox_ROIWidth, 12, 1)
        self.PyDMLabel_ROIWidth = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIWidth-RB')
        self.PyDMLabel_ROIWidth.setMaximumSize(220, 40)
        self.PyDMLabel_ROIWidth.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.PyDMLabel_ROIWidth, 12, 2)

        self.label = QLabel('ROI Heigth', self)
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label, 13, 1, 1, 2)
        self.PyDMSpinbox_ROIHeight = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIHeight-SP')
        self.PyDMSpinbox_ROIHeight.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIHeight.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIHeight.showStepExponent = False
        layout.addWidget(self.PyDMSpinbox_ROIHeight, 14, 1)
        self.PyDMLabel_ROIHeight = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIHeight-RB')
        self.PyDMLabel_ROIHeight.setMaximumSize(220, 40)
        self.PyDMLabel_ROIHeight.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.PyDMLabel_ROIHeight, 14, 2)

        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 15, 1)

        self.pushbutton_openCameraSettingsDetails = QPushButton(
            'Open details...', self)
        layout.addWidget(self.pushbutton_openCameraSettingsDetails, 16, 2)
        return layout

    def _statisticsLayout(self):
        layout = QGridLayout()
        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 1, 2)

        # - Method
        self.label_Method = QLabel('CalcMethod: ', self)
        self.label_Method.setMaximumHeight(40)
        layout.addWidget(self.label_Method, 2, 2)

        self.comboBox_Method = QComboBox(self)
        self.comboBox_Method.addItem('DimFei', 0)
        self.comboBox_Method.addItem('NDStats', 1)
        self.comboBox_Method.setCurrentIndex(0)
        self.comboBox_Method.currentIndexChanged.connect(
            self._handleShowStatistics)
        layout.addWidget(self.comboBox_Method, 2, 4)

        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 3, 2)

        # - Centroid
        self.label_Centroid = QLabel('Centroid', self)
        self.label_Centroid.setAlignment(Qt.AlignCenter)
        self.label_Centroid.setMaximumHeight(40)
        layout.addWidget(self.label_Centroid, 4, 1, 1, 5)
        self.label = QLabel('(', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 5, 1)

        self.PyDMLabel_CenterXDimFei = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CenterXDimFei-Mon')
        self.PyDMLabel_CenterXDimFei.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_CenterXDimFei.setMaximumSize(220, 40)
        layout.addWidget(self.PyDMLabel_CenterXDimFei, 5, 2)

        self.PyDMLabel_CenterXNDStats = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CenterXNDStats-Mon')
        self.PyDMLabel_CenterXNDStats.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_CenterXNDStats.setMaximumSize(220, 40)
        self.PyDMLabel_CenterXNDStats.setVisible(False)
        layout.addWidget(self.PyDMLabel_CenterXNDStats, 5, 2)

        self.label = QLabel(',', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 5, 3)

        self.PyDMLabel_CenterYDimFei = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CenterYDimFei-Mon')
        self.PyDMLabel_CenterYDimFei.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_CenterYDimFei.setMaximumSize(220, 40)
        layout.addWidget(self.PyDMLabel_CenterYDimFei, 5, 4)

        self.PyDMLabel_CenterYNDStats = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CenterYNDStats-Mon')
        self.PyDMLabel_CenterYNDStats.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_CenterYNDStats.setMaximumSize(220, 40)
        self.PyDMLabel_CenterYNDStats.setVisible(False)
        layout.addWidget(self.PyDMLabel_CenterYNDStats, 5, 4)

        self.label = QLabel(')', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 5, 5)

        # - Sigma
        self.label_Sigma = QLabel('Sigma', self)
        self.label_Sigma.setAlignment(Qt.AlignCenter)
        self.label_Sigma.setMaximumHeight(40)
        layout.addWidget(self.label_Sigma, 6, 1, 1, 5)
        self.label = QLabel('(', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 7, 1)

        self.PyDMLabel_SigmaXDimFei = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':SigmaXDimFei-Mon')
        self.PyDMLabel_SigmaXDimFei.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_SigmaXDimFei.setMaximumSize(220, 40)
        layout.addWidget(self.PyDMLabel_SigmaXDimFei, 7, 2)

        self.PyDMLabel_SigmaXNDStats = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':SigmaXNDStats-Mon')
        self.PyDMLabel_SigmaXNDStats.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_SigmaXNDStats.setMaximumSize(220, 40)
        self.PyDMLabel_SigmaXNDStats.setVisible(False)
        layout.addWidget(self.PyDMLabel_SigmaXNDStats, 7, 2)

        self.label = QLabel(',', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 7, 3)
        self.PyDMLabel_SigmaYDimFei = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':SigmaYDimFei-Mon')
        self.PyDMLabel_SigmaYDimFei.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_SigmaYDimFei.setMaximumSize(220, 40)

        layout.addWidget(self.PyDMLabel_SigmaYDimFei, 7, 4)
        self.PyDMLabel_SigmaYNDStats = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':SigmaYNDStats-Mon')
        self.PyDMLabel_SigmaYNDStats.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_SigmaYNDStats.setMaximumSize(220, 40)
        self.PyDMLabel_SigmaYNDStats.setVisible(False)
        layout.addWidget(self.PyDMLabel_SigmaYNDStats, 7, 4)

        self.label = QLabel(')', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 7, 5)

        # - Theta
        self.label_Theta = QLabel('Theta', self)
        self.label_Theta.setAlignment(Qt.AlignCenter)
        self.label_Theta.setMaximumHeight(40)
        layout.addWidget(self.label_Theta, 8, 1, 1, 5)
        self.label = QLabel('(', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 9, 1)
        self.PyDMLabel_ThetaDimFei = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ThetaDimFei-Mon')
        self.PyDMLabel_ThetaDimFei.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.PyDMLabel_ThetaDimFei, 9, 2, 1, 3)
        self.PyDMLabel_ThetaNDStats = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ThetaNDStats-Mon')
        self.PyDMLabel_ThetaNDStats.setAlignment(Qt.AlignHCenter)
        self.PyDMLabel_ThetaNDStats.setVisible(False)
        layout.addWidget(self.PyDMLabel_ThetaNDStats, 9, 2, 1, 3)
        self.label = QLabel(')', self)
        self.label.setMaximumSize(10, 40)
        layout.addWidget(self.label, 9, 5)

        layout.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 10, 2)
        return layout

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
        roi_h = self.PyDMLabel_ROIHeight.text()
        roi_w = self.PyDMLabel_ROIWidth.text()
        roi_offsetx = self.PyDMLabel_ROIOffsetX.text()
        roi_offsety = self.PyDMLabel_ROIOffsetY.text()
        self.PyDMSpinbox_ROIHeight.value_changed(
                self.image_view.image_maxheight)
        self.PyDMSpinbox_ROIHeight.send_value()
        self.PyDMSpinbox_ROIWidth.value_changed(
                self.image_view.image_maxwidth)
        self.PyDMSpinbox_ROIWidth.send_value()
        self.PyDMSpinbox_ROIOffsetX.value_changed(0)
        self.PyDMSpinbox_ROIOffsetX.send_value()
        self.PyDMSpinbox_ROIOffsetY.value_changed(0)
        self.PyDMSpinbox_ROIOffsetY.send_value()
        self.image_view.saveCalibrationGrid()
        self.PyDMSpinbox_ROIHeight.value_changed(int(roi_h))
        self.PyDMSpinbox_ROIHeight.send_value()
        self.PyDMSpinbox_ROIWidth.value_changed(int(roi_w))
        self.PyDMSpinbox_ROIWidth.send_value()
        self.PyDMSpinbox_ROIOffsetX.value_changed(int(roi_offsetx))
        self.PyDMSpinbox_ROIOffsetX.send_value()
        self.PyDMSpinbox_ROIOffsetY.value_changed(int(roi_offsety))
        self.PyDMSpinbox_ROIOffsetY.send_value()
        time.sleep(0.1)

    @pyqtSlot()
    def _showFailToSaveGridMsg(self):
        QMessageBox.warning(self, 'Warning',
                            'Could not save calibration grid!',
                            QMessageBox.Ok)

    @pyqtSlot()
    def _zoomIn(self):
        """Zoom ImageView to 0.5x current image scale."""
        self.image_view.getView().scaleBy((0.5, 0.5))

    @pyqtSlot()
    def _zoomOut(self):
        """Zoom ImageView to 2x current image scale."""
        self.image_view.getView().scaleBy((2.0, 2.0))

    @pyqtSlot()
    def _zoomToActualSize(self):
        """Zoom ImqgeView to actual image size."""
        if len(self.image_view.image_waveform) == 0:
            return
        self.image_view.getView().setRange(
            xRange=(0, self.image_view.imageWidth),
            yRange=(0, self.image_view.image_waveform.shape[0] /
                    self.image_view.imageWidth))


class _CameraSettingsDetails(SiriusMainWindow):

    def __init__(self, parent=None, device=None, prefix=None):
        super(SiriusMainWindow, self).__init__(parent=parent)
        self.prefix = prefix
        self.device = device
        self.setWindowTitle('Camera Settings Details')
        self.centralwidget = QWidget(self)
        self.centralwidget.setLayout(QFormLayout())
        self.centralwidget.layout().setLabelAlignment(Qt.AlignRight)
        self._setupUi()
        self.setCentralWidget(self.centralwidget)

    def _setupUi(self):
        label = QLabel('Camera Acquire Settings')
        label.setStyleSheet("""font-weight: bold;""")
        self.centralwidget.layout().addRow(label)

        self.centralwidget.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))

        hbox = QHBoxLayout()
        self.label_AcqEnbl = QLabel('Acquire Enable Status', self)
        self.PyDMStateButton_AcqEnbl = PyDMStateButton(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamEnbl-Sel')
        self.PyDMStateButton_AcqEnbl.setMaximumSize(220, 40)
        self.PyDMLabel_AcqEnbl = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamEnbl-Sts')
        self.PyDMLabel_AcqEnbl.setMaximumSize(220, 40)
        self.PyDMLabel_AcqEnbl.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMStateButton_AcqEnbl)
        hbox.addWidget(self.PyDMLabel_AcqEnbl)
        self.centralwidget.layout().addRow(self.label_AcqEnbl, hbox)

        hbox = QHBoxLayout()
        self.label_AcqMode = QLabel('Acquire Mode', self)
        self.PyDMEnumComboBox_AcqMode = PyDMEnumComboBox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamAcqMode-SP')
        self.PyDMEnumComboBox_AcqMode.setMaximumSize(220, 40)
        self.PyDMLabel_AcqMode = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamAcqMode-RB')
        self.PyDMLabel_AcqMode.setMaximumSize(220, 40)
        self.PyDMLabel_AcqMode.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMEnumComboBox_AcqMode)
        hbox.addWidget(self.PyDMLabel_AcqMode)
        self.centralwidget.layout().addRow(self.label_AcqMode, hbox)

        hbox = QHBoxLayout()
        self.label_AcqPeriod = QLabel('Acquire Period', self)
        self.PyDMSpinbox_AcqPeriod = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamAcqPeriod-SP')
        self.PyDMSpinbox_AcqPeriod.setMaximumSize(220, 40)
        self.PyDMSpinbox_AcqPeriod.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_AcqPeriod.showStepExponent = False
        self.PyDMLabel_AcqPeriod = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamAcqPeriod-RB')
        self.PyDMLabel_AcqPeriod.setMaximumSize(220, 40)
        self.PyDMLabel_AcqPeriod.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_AcqPeriod)
        hbox.addWidget(self.PyDMLabel_AcqPeriod)
        self.centralwidget.layout().addRow(self.label_AcqPeriod, hbox)

        hbox = QHBoxLayout()
        self.label_Gain = QLabel('Gain', self)
        self.PyDMSpinbox_Gain = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamGain-SP')
        self.PyDMSpinbox_Gain.setMinimumSize(220, 40)
        self.PyDMSpinbox_Gain.setMaximumSize(220, 40)
        self.PyDMSpinbox_Gain.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_Gain.showStepExponent = False
        self.PyDMLabel_Gain = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamGain-RB')
        self.PyDMLabel_Gain.setMinimumSize(220, 40)
        self.PyDMLabel_Gain.setMaximumSize(220, 40)
        self.PyDMLabel_Gain.setAlignment(Qt.AlignCenter)
        self.PyDMPushButton_AutoGain = PyDMPushButton(
            parent=self,
            label='Auto Gain',
            pressValue=1,
            init_channel='ca://'+self.prefix+self.device+':CamAutoGain-Cmg')
        self.PyDMPushButton_AutoGain.setMaximumSize(220, 40)
        hbox.addWidget(self.PyDMSpinbox_Gain)
        hbox.addWidget(self.PyDMLabel_Gain)
        hbox.addWidget(self.PyDMPushButton_AutoGain)
        self.centralwidget.layout().addRow(self.label_Gain, hbox)

        hbox = QHBoxLayout()
        self.label_BlackLevel = QLabel('Black Level', self)
        self.PyDMSpinbox_BlackLevel = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamBlackLevel-SP')
        self.PyDMSpinbox_BlackLevel.setMaximumSize(220, 40)
        self.PyDMSpinbox_BlackLevel.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_BlackLevel.showStepExponent = False
        self.PyDMLabel_BlackLevel = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamBlackLevel-RB')
        self.PyDMLabel_BlackLevel.setMaximumSize(220, 40)
        self.PyDMLabel_BlackLevel.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_BlackLevel)
        hbox.addWidget(self.PyDMLabel_BlackLevel)
        self.centralwidget.layout().addRow(self.label_BlackLevel, hbox)

        hbox = QHBoxLayout()
        self.label_DebPeriod = QLabel('Trigger Debouncer Period', self)
        self.PyDMSpinbox_DebPeriod = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device +
                         ':CamDebouncerPeriod-SP')
        self.PyDMSpinbox_DebPeriod.setMaximumSize(220, 40)
        self.PyDMSpinbox_DebPeriod.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_DebPeriod.showStepExponent = False
        self.PyDMLabel_DebPeriod = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device +
                         ':CamDebouncerPeriod-RB')
        self.PyDMLabel_DebPeriod.setMaximumSize(220, 40)
        self.PyDMLabel_DebPeriod.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_DebPeriod)
        hbox.addWidget(self.PyDMLabel_DebPeriod)
        self.centralwidget.layout().addRow(self.label_DebPeriod, hbox)

        hbox = QHBoxLayout()
        self.label_ExpMode = QLabel('Exposure Mode', self)
        self.PyDMEnumComboBox_ExpMode = PyDMEnumComboBox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamExposureMode-SP')
        self.PyDMEnumComboBox_ExpMode.setMaximumSize(220, 40)
        self.PyDMLabel_ExpMode = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamExposureMode-RB')
        self.PyDMLabel_ExpMode.setMaximumSize(220, 40)
        self.PyDMLabel_ExpMode.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMEnumComboBox_ExpMode)
        hbox.addWidget(self.PyDMLabel_ExpMode)
        self.centralwidget.layout().addRow(self.label_ExpMode, hbox)

        hbox = QHBoxLayout()
        self.label_ExpTime = QLabel('Exposure Time', self)
        self.PyDMSpinbox_ExpTime = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamExposureTime-SP')
        self.PyDMSpinbox_ExpTime.setMaximumSize(220, 40)
        self.PyDMSpinbox_ExpTime.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ExpTime.showStepExponent = False
        self.PyDMLabel_ExpTime = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':CamExposureTime-RB')
        self.PyDMLabel_ExpTime.setMaximumSize(220, 40)
        self.PyDMLabel_ExpTime.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_ExpTime)
        hbox.addWidget(self.PyDMLabel_ExpTime)
        self.centralwidget.layout().addRow(self.label_ExpTime, hbox)

        self.centralwidget.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))

        label = QLabel('Camera Region of Interest (ROI) Settings')
        label.setStyleSheet("""font-weight: bold;""")
        self.centralwidget.layout().addRow(label)

        self.centralwidget.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))

        hbox = QHBoxLayout()
        self.label_ROIOffsetX = QLabel('Offset X', self)
        self.PyDMSpinbox_ROIOffsetX = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetX-SP')
        self.PyDMSpinbox_ROIOffsetX.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIOffsetX.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIOffsetX.showStepExponent = False
        self.PyDMLabel_ROIOffsetX = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetX-RB')
        self.PyDMLabel_ROIOffsetX.setMaximumSize(220, 40)
        self.PyDMLabel_ROIOffsetX.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_ROIOffsetX)
        hbox.addWidget(self.PyDMLabel_ROIOffsetX)
        self.centralwidget.layout().addRow(self.label_ROIOffsetX, hbox)

        hbox = QHBoxLayout()
        self.label_ROIOffsetY = QLabel('Offset Y', self)
        self.PyDMSpinbox_ROIOffsetY = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetY-SP')
        self.PyDMSpinbox_ROIOffsetY.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIOffsetY.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIOffsetY.showStepExponent = False
        self.PyDMLabel_ROIOffsetY = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIOffsetY-RB')
        self.PyDMLabel_ROIOffsetY.setMaximumSize(220, 40)
        self.PyDMLabel_ROIOffsetY.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_ROIOffsetY)
        hbox.addWidget(self.PyDMLabel_ROIOffsetY)
        self.centralwidget.layout().addRow(self.label_ROIOffsetY, hbox)

        hbox = QHBoxLayout()
        self.label_ROIWidth = QLabel('Width', self)
        self.PyDMSpinbox_ROIWidth = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIWidth-SP')
        self.PyDMSpinbox_ROIWidth.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIWidth.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIWidth.showStepExponent = False
        self.PyDMLabel_ROIWidth = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIWidth-RB')
        self.PyDMLabel_ROIWidth.setMaximumSize(220, 40)
        self.PyDMLabel_ROIWidth.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_ROIWidth)
        hbox.addWidget(self.PyDMLabel_ROIWidth)
        self.centralwidget.layout().addRow(self.label_ROIWidth, hbox)

        hbox = QHBoxLayout()
        self.label_ROIHeight = QLabel('Heigth', self)
        self.PyDMSpinbox_ROIHeight = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIHeight-SP')
        self.PyDMSpinbox_ROIHeight.setMaximumSize(220, 40)
        self.PyDMSpinbox_ROIHeight.setAlignment(Qt.AlignCenter)
        self.PyDMSpinbox_ROIHeight.showStepExponent = False
        self.PyDMLabel_ROIHeight = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':ImgROIHeight-RB')
        self.PyDMLabel_ROIHeight.setMaximumSize(220, 40)
        self.PyDMLabel_ROIHeight.setAlignment(Qt.AlignCenter)
        hbox.addWidget(self.PyDMSpinbox_ROIHeight)
        hbox.addWidget(self.PyDMLabel_ROIHeight)
        self.centralwidget.layout().addRow(self.label_ROIHeight, hbox)

        self.centralwidget.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))

        label = QLabel('Camera Errors Monitoring')
        label.setStyleSheet("""font-weight: bold;""")
        self.centralwidget.layout().addRow(label)

        self.centralwidget.layout().addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))

        hbox = QHBoxLayout()
        self.label_LastErr = QLabel('Last Error', self)
        self.PyDMLabel_LastErr = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+self.device+':LastErr-Mon')
        self.PyDMLabel_LastErr.setAlignment(Qt.AlignCenter)
        self.PyDMLabel_LastErr.setMinimumSize(440, 40)
        self.PyDMPushButton_LastErr = PyDMPushButton(
            parent=self,
            label='Clear Last Error',
            pressValue=1,
            init_channel='ca://'+self.prefix+self.device+':ClearLastErr-Cmd')
        self.PyDMPushButton_LastErr.setMaximumSize(220, 40)
        hbox.addWidget(self.PyDMLabel_LastErr)
        hbox.addWidget(self.PyDMPushButton_LastErr)
        self.centralwidget.layout().addRow(self.label_LastErr, hbox)