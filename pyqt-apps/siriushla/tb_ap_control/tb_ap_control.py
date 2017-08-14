#!/usr/bin/env python3.6
from pydm.PyQt.uic import loadUi
from pydm.PyQt.QtCore import pyqtSlot, Qt
from pydm.PyQt.QtGui import (QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QSizePolicy, QDoubleValidator,
                            QWidget, QFrame, QLabel, QPixmap, QPushButton, QSpacerItem, QApplication)
from pydm import PyDMApplication
from pydm.widgets.led import PyDMLed
from pydm.widgets.label import PyDMLabel
from pydm.widgets.line_edit import PyDMLineEdit
from pydm.widgets.scrollbar import PyDMScrollBar
from pydm.widgets.enum_combo_box import PyDMEnumComboBox
from pydm.widgets.checkbox import PyDMCheckbox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from pydm.PyQt.QtSvg import QSvgWidget
import sys
import socket
import pyaccel as _pyaccel
import pymodels as _pymodels
from siriushla.as_ma_control.MagnetDetailWindow import MagnetDetailWindow
from siriushla.as_ma_control import ToBoosterMagnetControlWindow
from siriushla.tb_ap_posang.tb_ap_posang import LTBPosAngCorr


CALC_LABELS_INITIALIZE = """
self.centralwidget.PyDMEnumComboBox_CalcMethod_Scrn{0}.currentIndexChanged.connect(self._visibility_handle)
"""

CALC_LABELS_VISIBILITY = """
self.centralwidget.PyDMLabel_CenterXDimfei_Scrn{0}.setVisible(visible)
self.centralwidget.PyDMLabel_CenterXNDStats_Scrn{0}.setVisible(not visible)
self.centralwidget.PyDMLabel_CenterYDimfei_Scrn{0}.setVisible(visible)
self.centralwidget.PyDMLabel_CenterYNDStats_Scrn{0}.setVisible(not visible)
self.centralwidget.PyDMLabel_ThetaDimfei_Scrn{0}.setVisible(visible)
self.centralwidget.PyDMLabel_ThetaNDStats_Scrn{0}.setVisible(not visible)
self.centralwidget.PyDMLabel_SigmaXDimfei_Scrn{0}.setVisible(visible)
self.centralwidget.PyDMLabel_SigmaXNDStats_Scrn{0}.setVisible(not visible)
self.centralwidget.PyDMLabel_SigmaYDimfei_Scrn{0}.setVisible(visible)
self.centralwidget.PyDMLabel_SigmaYNDStats_Scrn{0}.setVisible(not visible)
"""


class LTBControlWindow(QMainWindow):
    def __init__(self, parent=None):
        super(LTBControlWindow, self).__init__(parent)
        self.centralwidget = loadUi('/home/fac_files/lnls-sirius/hla/pyqt-apps/siriushla/tb_ap_control/ui_tb_ap_control.ui')
        self.setCentralWidget(self.centralwidget)

        # Estabilish widget connections
        self.app = QApplication.instance()
        self.app.establish_widget_connections(self)

        #TB Lattice Widget
        lattice = QSvgWidget('LTB.svg')
        self.centralwidget.widget_lattice.setLayout(QVBoxLayout())
        self.centralwidget.widget_lattice.layout().addWidget(lattice)

        #TB Optics Widget
        self.lattice_and_twiss_window = ShowLatticeAndTwiss()
        self.centralwidget.pushButton_LatticeAndTwiss.clicked.connect(self._openLaticeAndTwiss)

        #Set Visibility of Labels
        for i in [11, 12, 21, 22, 3, 4]:
            exec(CALC_LABELS_INITIALIZE.format(i))
            visible = True
            exec(CALC_LABELS_VISIBILITY.format(i))

        #Reference Widget
        self.centralwidget.tabWidget_Scrns.setCurrentIndex(0)
        self._currScrn = 0
        self.reference_window = ShowImage()
        self.centralwidget.tabWidget_Scrns.currentChanged.connect(self._setCurrentScrn)
        self.centralwidget.pushButton_SaveRef.clicked.connect(self._saveReference)
        self.centralwidget.pushButton_OpenRef.clicked.connect(self._openReference)

        #Open LTBApps
        self.centralwidget.pushButton_LTB_MAApp.clicked.connect(self._openMAApp)
        self.centralwidget.pushButton_LTB_BPMApp.clicked.connect(self._openBPMApp)
        self.centralwidget.pushButton_FCTApp.clicked.connect(self._openFCTApp)
        self.centralwidget.pushButton_LTB_PosAngleCorrApp.clicked.connect(self._openPosAngleCorrApp)
        self.centralwidget.pushButton_SplitApp.clicked.connect(self._openSplitApp)

        #Create Scrn+Correctors Panel
        scrn_headerline = QWidget()
        scrn_headerline.setLayout(QHBoxLayout())
        scrn_headerline.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_scrn = QLabel('Scrn')
        label_scrn.setAlignment(Qt.AlignHCenter)
        label_scrn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_position = QLabel('Position')
        label_position.setAlignment(Qt.AlignHCenter)
        label_position.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_lamp = QLabel('Lamp')
        label_lamp.setAlignment(Qt.AlignHCenter)
        label_lamp.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        scrn_headerline.layout().addWidget(label_scrn)
        scrn_headerline.layout().addWidget(label_position)
        scrn_headerline.layout().addWidget(label_lamp)
        scrn_headerline.layout().setContentsMargins(0,0,0,0)
        # scrn_headerline.setStyleSheet('''QLabel{background-color:blue;}''')

        ch_headerline = QWidget()
        ch_headerline.setLayout(QHBoxLayout())
        ch_headerline.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_ch_led = QLabel('')
        label_ch_led.setAlignment(Qt.AlignHCenter)
        label_ch_led.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_ch = QLabel('CH')
        label_ch.setAlignment(Qt.AlignHCenter)
        label_ch.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_ch.setStyleSheet("""font-size:16pt""")
        label_ch_sp_kick = QLabel('Kick-SP')
        label_ch_sp_kick.setAlignment(Qt.AlignHCenter)
        label_ch_sp_kick.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        label_ch_mon_kick = QLabel('Kick-Mon')
        label_ch_mon_kick.setAlignment(Qt.AlignHCenter)
        label_ch_mon_kick.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        ch_headerline.layout().addWidget(label_ch_led)
        ch_headerline.layout().addWidget(label_ch)
        ch_headerline.layout().addWidget(label_ch_sp_kick)
        ch_headerline.layout().addWidget(label_ch_mon_kick)
        ch_headerline.layout().setContentsMargins(0,0,0,0)
        # ch_headerline.setStyleSheet('''QLabel{background-color:blue;}''')

        cv_headerline = QWidget()
        cv_headerline.setLayout(QHBoxLayout())
        cv_headerline.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_cv_led = QLabel('')
        label_cv_led.setAlignment(Qt.AlignHCenter)
        label_cv_led.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_cv = QLabel('CV')
        label_cv.setAlignment(Qt.AlignHCenter)
        label_cv.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        label_cv.setStyleSheet("""font-size:16pt""")
        label_cv_sp_kick = QLabel('Kick-SP')
        label_cv_sp_kick.setAlignment(Qt.AlignHCenter)
        label_cv_sp_kick.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        label_cv_mon_kick = QLabel('Kick-Mon')
        label_cv_mon_kick.setAlignment(Qt.AlignHCenter)
        label_cv_mon_kick.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        cv_headerline.layout().addWidget(label_cv_led)
        cv_headerline.layout().addWidget(label_cv)
        cv_headerline.layout().addWidget(label_cv_sp_kick)
        cv_headerline.layout().addWidget(label_cv_mon_kick)
        cv_headerline.layout().setContentsMargins(0,0,0,0)
        # cv_headerline.setStyleSheet('''QLabel{background-color:blue;}''')

        headerline = QWidget()
        headerline.setMaximumHeight(40)
        headerline.setLayout(QHBoxLayout())
        headerline.layout().addWidget(scrn_headerline)
        headerline.layout().addItem(QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum))
        headerline.layout().addWidget(ch_headerline)
        headerline.layout().addItem(QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum))
        headerline.layout().addWidget(cv_headerline)
        headerline.setStyleSheet("""font-weight:bold;""")
        headerline.layout().setContentsMargins(0,9,0,9)
        correctors_gridlayout = QGridLayout()
        correctors_gridlayout.addWidget(headerline,1,1)
        for item,width in [[label_scrn,100],[label_position,110],[label_lamp,118],
                           [label_ch_led,24],[label_ch,100],[label_ch_sp_kick,180],[label_ch_mon_kick,100],
                           [label_cv_led,24],[label_cv,100],[label_cv_sp_kick,180],[label_cv_mon_kick,100]]:
            item.setMaximumWidth(width)
            item.setMinimumWidth(width)

        line = 2
        for ch,cv,scrn,scrnpv in [['01:MA-CH-7','01:MA-CV-7',11,'01:DI-Scrn-1'],\
                                 ['01:MA-CH-1','01:MA-CV-1',12,'01:DI-Scrn-2'],\
                                 ['01:MA-CH-2','01:MA-CV-2',21,'02:DI-Scrn-1'],\
                                 ['02:MA-CH-1','02:MA-CV-1',22,'02:DI-Scrn-2'],\
                                 ['02:MA-CH-2','02:MA-CV-2',3,'03:DI-Scrn'],\
                                 ['03:MA-CH','04:MA-CV-1',4,'04:DI-Scrn']]:
            if scrn == 11:
                acc = 'LI-'
            else:
                acc = 'TB-'
            #Scrn
            scrn_details = QWidget()
            scrn_details.setObjectName('widget_Scrn' + str(scrn))
            scrn_details.setLayout(QHBoxLayout())
            scrn_details.layout().setContentsMargins(3,3,3,3)

            scrn_label = QLabel(scrnpv)
            scrn_label.setMinimumWidth(100)
            scrn_label.setStyleSheet("""font-weight:bold;""")
            scrn_details.layout().addWidget(scrn_label)

            widget_position_sp = QWidget()
            widget_position_sp.setLayout(QVBoxLayout())
            widget_position_sp.layout().setContentsMargins(0,0,0,0)
            pydmcombobox_position = PyDMEnumComboBox(scrn_details,'ca://' + 'fac-' + socket.gethostname() + '-' + acc + scrnpv + ':Position-SP')
            pydmcombobox_position.setObjectName('PyDMEnumComboBox_Position_SP_Scrn' + str(scrn))
            widget_position_sp.layout().addWidget(pydmcombobox_position)
            pydmcombobox_position_items = [pydmcombobox_position.itemText(i) for i in range(pydmcombobox_position.count())]
            pydmled_position = PyDMLed(scrn_details,'ca://' + 'fac-' + socket.gethostname() + '-' + acc + scrnpv + ':Position-Mon')
                                    #    enum_map={pydmcombobox_position_items[0]:-1,pydmcombobox_position_items[1]: 2,pydmcombobox_position_items[2]:0})#TODO
            pydmled_position.setObjectName('PyDMLed_Position_Mon_Scrn' + str(scrn))
            pydmled_position.shape = 2
            pydmled_position.setMinimumWidth(110)
            pydmled_position.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            # pydmlabel_position = PyDMLabel(scrn_details, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + scrnpv + ':Position-Mon')
            # pydmlabel_position.setObjectName('PyDMLabel_Position_Mon_Scrn' + str(scrn))
            # pydmlabel_position.setMinimumWidth(80)
            # frame_label = QFrame()
            # frame_label.setFrameShadow(QFrame.Raised)
            # frame_label.setFrameShape(QFrame.Box)
            # frame_label.setLayout(QVBoxLayout())
            # frame_label.layout().setContentsMargins(3,3,3,3)
            # frame_label.setMinimumHeight(28)
            # frame_label.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
            # frame_label.layout().addWidget(pydmlabel_position)
            # widget_position_sp.layout().addWidget(frame_label)
            widget_position_sp.layout().addWidget(pydmled_position)
            widget_position_sp.setMinimumWidth(110)
            widget_position_sp.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            scrn_details.layout().addWidget(widget_position_sp)

            scrn_details.layout().addItem(QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum))
            pydmcheckbox = PyDMCheckbox(scrn_details, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + scrnpv + ':LampState-SP')
            pydmcheckbox.setObjectName('PyDMCheckbox_LampState_SP_Scrn' + str(scrn))
            pydmcheckbox.setMinimumWidth(14)
            pydmcheckbox.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
            scrn_details.layout().addWidget(pydmcheckbox)
            pydmled = PyDMLed(scrn_details,'ca://' + 'fac-' + socket.gethostname() + '-' + acc + scrnpv + ':LampState-Sts')
            pydmled.setObjectName('PyDMLed_LampState_Sts_Scrn' + str(scrn))
            pydmled.setMinimumWidth(24)
            pydmled.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
            scrn_details.layout().addWidget(pydmled)
            scrn_details.layout().addItem(QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum))

            #Correctors
            name = ch.split('-')
            if len(name) > 3:
                name = name[-2]+name[-1]
            else:
                name = name[-1]

            ch_details = QWidget()
            ch_details.setObjectName('widget_details_' + name + '_Scrn' + str(scrn))
            ch_details.setLayout(QGridLayout())
            ch_details.layout().setContentsMargins(3,3,3,3)

            pydmled = PyDMLed(ch_details,'ca://' + 'fac-' + socket.gethostname() + '-' + acc + ch + ':PwrState-Sts')
            pydmled.setObjectName('PyDMLed_' + name + '_PwrState' + '_Scrn' + str(scrn))
            pydmled.setMinimumWidth(24)
            pydmled.setMinimumHeight(24)
            pydmled.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
            ch_details.layout().addWidget(pydmled,1,1)

            pushbutton = QPushButton(ch, ch_details)
            pushbutton.setObjectName('pushButton_' + name + 'App_Scrn' + str(scrn))
            pushbutton.clicked.connect(self._openWindow)
            pushbutton.setMinimumWidth(100)
            pushbutton.setMinimumHeight(24)
            pushbutton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
            ch_details.layout().addWidget(pushbutton,1,2)

            pydmlineedit_kick = PyDMLineEdit(ch_details, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + ch + ':Kick-SP')
            pydmlineedit_kick.setObjectName('PyDMLineEdit' + name + '_Kick_SP_Scrn' + str(scrn))
            pydmlineedit_kick.setValidator(QDoubleValidator())
            pydmlineedit_kick._useunits = False
            pydmlineedit_kick.setMinimumWidth(180)
            pydmlineedit_kick.setMinimumHeight(24)
            pydmlineedit_kick.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
            ch_details.layout().addWidget(pydmlineedit_kick,1,5)

            scrollbar_kick = PyDMScrollBar(ch_details, Qt.Horizontal, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + ch + ':Kick-SP')
            scrollbar_kick.setObjectName('PyDMScrollBar' + name + '_Kick_SP_Scrn' + str(scrn))
            scrollbar_kick.setMinimumWidth(180)
            scrollbar_kick.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
            scrollbar_kick.limitsFromPV = True
            ch_details.layout().addWidget(scrollbar_kick,2,5)

            pydmlabel_kick = PyDMLabel(ch_details, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + ch + ':Kick-Mon')
            pydmlabel_kick.setObjectName('PyDMLabel_' + name + '_Kick_Mon_Scrn' + str(scrn))
            pydmlabel_kick.setMinimumWidth(100)
            pydmlabel_kick.setMinimumHeight(28)
            pydmlabel_kick.precFromPV = True
            pydmlabel_kick.setFrameShadow(QFrame.Raised)
            pydmlabel_kick.setFrameShape(QFrame.Box)
            pydmlabel_kick.setLayout(QVBoxLayout())
            pydmlabel_kick.layout().setContentsMargins(3,3,3,3)
            pydmlabel_kick.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            ch_details.layout().addWidget(pydmlabel_kick,1,6)
            ch_details.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)

            name = cv.split('-')
            if len(name) > 3:
                name = name[-2]+name[-1]
            else:
                name = name[-1]

            cv_details = QWidget()
            cv_details.setObjectName('widget_details_' + name + '_Scrn' + str(scrn))
            cv_details.setLayout(QGridLayout())
            cv_details.layout().setContentsMargins(3,3,3,3)

            pydmled = PyDMLed(cv_details,'ca://' + 'fac-' + socket.gethostname() + '-' + acc + cv + ':PwrState-Sts')
            pydmled.setObjectName('PyDMLed_' + name + '_PwrState' + '_Scrn' + str(scrn))
            pydmled.setMinimumWidth(24)
            pydmled.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
            cv_details.layout().addWidget(pydmled,1,1)

            pushbutton = QPushButton(cv, cv_details)
            pushbutton.setObjectName('pushButton_' + name + 'App_Scrn' + str(scrn))
            pushbutton.clicked.connect(self._openWindow)
            pushbutton.setMinimumWidth(100)
            pushbutton.setMinimumHeight(24)
            pushbutton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
            cv_details.layout().addWidget(pushbutton,1,2)

            pydmlineedit_kick = PyDMLineEdit(cv_details, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + cv + ':Kick-SP')
            pydmlineedit_kick.setObjectName('PyDMLineEdit' + name + '_Kick_SP_Scrn' + str(scrn))
            pydmlineedit_kick.setValidator(QDoubleValidator())
            pydmlineedit_kick._useunits = False
            pydmlineedit_kick.setMinimumWidth(180)
            pydmlineedit_kick.setMinimumHeight(24)
            pydmlineedit_kick.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
            cv_details.layout().addWidget(pydmlineedit_kick,1,5)

            scrollbar_kick = PyDMScrollBar(cv_details, Qt.Horizontal, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + cv + ':Kick-SP')
            scrollbar_kick.setObjectName('PyDMScrollBar' + name + '_Kick_SP_Scrn' + str(scrn))
            scrollbar_kick.setMinimumWidth(180)
            scrollbar_kick.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
            scrollbar_kick.limitsFromPV = True
            cv_details.layout().addWidget(scrollbar_kick,2,5)

            pydmlabel_kick = PyDMLabel(cv_details, 'ca://' + 'fac-' + socket.gethostname() + '-' + acc + cv + ':Kick-Mon')
            pydmlabel_kick.setObjectName('PyDMLabel_' + name + '_Kick_Mon_Scrn' + str(scrn))
            pydmlabel_kick.setMinimumWidth(100)
            pydmlabel_kick.setMinimumHeight(28)
            pydmlabel_kick.precFromPV = True
            pydmlabel_kick.setFrameShadow(QFrame.Raised)
            pydmlabel_kick.setFrameShape(QFrame.Box)
            pydmlabel_kick.setLayout(QVBoxLayout())
            pydmlabel_kick.layout().setContentsMargins(3,3,3,3)
            pydmlabel_kick.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            cv_details.layout().addWidget(pydmlabel_kick,1,6)
            cv_details.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)

            widget_scrnch = QWidget()
            widget_scrnch.setLayout(QHBoxLayout())
            widget_scrnch.layout().addWidget(scrn_details)
            widget_scrnch.layout().addItem(QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum))
            widget_scrnch.layout().addWidget(ch_details)
            widget_scrnch.layout().addItem(QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum))
            widget_scrnch.layout().addWidget(cv_details)
            widget_scrnch.layout().setContentsMargins(2,2,2,2)

            if line%2 == 0:
                widget_scrnch.setStyleSheet("""background-color: rgb(211, 211, 211);""")
            correctors_gridlayout.addWidget(widget_scrnch,line,1)
            line += 1

        self.centralwidget.groupBox_allcorrectorsPanel.setLayout(correctors_gridlayout)
        self.centralwidget.groupBox_allcorrectorsPanel.layout().setContentsMargins(2,2,2,2)

    @pyqtSlot(int)
    def _visibility_handle(self,index):
        if index == 0:  visible = True
        else:           visible = False

        if self._currScrn == 0:     scrn = 11
        elif self._currScrn == 1:   scrn = 12
        elif self._currScrn == 2:   scrn = 21
        elif self._currScrn == 3:   scrn = 22
        elif self._currScrn == 4:   scrn = 3
        elif self._currScrn == 5:   scrn = 4

        exec(CALC_LABELS_VISIBILITY.format(scrn))

    @pyqtSlot(int)
    def _setCurrentScrn(self,currScrn):
        self._currScrn = currScrn

    def _openReference(self):
        fn, _ = QFileDialog.getOpenFileName(self, 'Open Reference...', None,
                'Images (*.png *.xpm *.jpg);;All Files (*)')
        if fn:
            self.reference_window.load_image(fn)
            self.reference_window.show()

    def _saveReference(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Save Reference As...', None,
                'Images (*.png *.xpm *.jpg);;All Files (*)')
        if not fn: return False
        lfn = fn.lower()
        if not lfn.endswith(('.png', '.jpg', '.xpm')): fn += '.png'

        if self._currScrn == 0:
            reference = self.centralwidget.widget_Scrn11.grab()
        elif self._currScrn == 1:
            reference = self.centralwidget.widget_Scrn12.grab()
        elif self._currScrn == 2:
            reference = self.centralwidget.widget_Scrn21.grab()
        elif self._currScrn == 3:
            reference = self.centralwidget.widget_Scrn22.grab()
        elif self._currScrn == 4:
            reference = self.centralwidget.widget_Scrn3.grab()
        elif self._currScrn == 5:
            reference = self.centralwidget.widget_Scrn4.grab()
        reference.save(fn)

    def _openWindow(self):
        sender = self.sender()

        if sender.text().split('-')[0] == 'LI':
            pass
            #TODO
        else:
            ma = 'TB-' + sender.text()
            self._corrector_detail_window = MagnetDetailWindow(ma,self)
            self._corrector_detail_window.show()

    def _openMAApp(self):
        self._LTB_MA_window = ToBoosterMagnetControlWindow(self)
        self._LTB_MA_window.show()

    def _openBPMApp(self):
        pass
        #TODO

    def _openFCTApp(self):
        pass
        #TODO

    def _openPosAngleCorrApp(self):
        self._LTB_PosAng_window = LTBPosAngCorr(self)
        self._LTB_PosAng_window.show()

    def _openLaticeAndTwiss(self):
        self.lattice_and_twiss_window.show()

    def _openSplitApp(self):
        pass
        #TODO

    # @pyqtSlot(int)
    # def _setBackgroundcolor2Position(self,position):
    #     sender = self.sender()
    #     scrn = self.comboboxlist.index(sender)
    #     if position == 0: #home
    #         self.framelist[scrn].setStyleSheet("""""")
    #     elif position == 1: #pos1
    #         self.framelist[scrn].setStyleSheet("""background-color:red""")
    #     elif position == 2: #pos2
    #         self.framelist[scrn].setStyleSheet("""background-color:yellow""")

    def closeEvent(self, event):
        """Reimplement close event to close widget connections."""
        self.app.close_widget_connections(self)
        super().closeEvent(event)

class ShowLatticeAndTwiss(QWidget):
    def __init__(self,parent=None):
        super(ShowLatticeAndTwiss, self).__init__(parent)
        self._tb,self._twiss_in = _pymodels.tb.create_accelerator()
        self._tb_twiss, *_ = _pyaccel.optics.calc_twiss(accelerator=self._tb,init_twiss=self._twiss_in)
        fam_data = _pymodels.tb.families.get_family_data(self._tb)
        fam_mapping = _pymodels.tb.family_mapping
        self._fig,self._ax = _pyaccel.graphics.plot_twiss(accelerator=self._tb,twiss=self._tb_twiss,
                                                            family_data=fam_data, family_mapping=fam_mapping,
                                                            draw_edges=True,height=4,show_label=True)
        self.canvas = FigureCanvas(self._fig)
        self.canvas.setParent(self)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        self.setLayout(self.vbox)
        self.layout().setContentsMargins(0,0,0,0)
        self.setGeometry(10,10,1500,400)


class ShowImage(QWidget):
    def __init__(self, parent=None):
        super(ShowImage, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.label = QLabel()
        self.layout().addWidget(self.label)

    def load_image(self,filename):
        self.setWindowTitle(filename)
        self.pixmap = QPixmap(filename)
        self.label.setPixmap(self.pixmap)
        self.setGeometry(300,300,self.pixmap.width(),self.pixmap.height())

if __name__ == '__main__':
    app = PyDMApplication(None, sys.argv)
    window = LTBControlWindow()
    window.show()
    sys.exit(app.exec_())
