from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from pydm import PyDMApplication
#from test import Ui_MainWindow
import sys

app = PyDMApplication()
#app = QApplication([])
#main_win = QMainWindow()
#uii = Ui_MainWindow()
#uii.setupUi(main_win)
main_win = uic.loadUi('main_window.ui')
main_win.show()
sys.exit(app.exec_())


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1409, 203)
        self.widget_12 = QtWidgets.QWidget(Form)
        self.widget_12.setGeometry(QtCore.QRect(180, 140, 1146, 44))
        self.widget_12.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_187 = QtWidgets.QHBoxLayout(self.widget_12)
        self.horizontalLayout_187.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_187.setObjectName("horizontalLayout_187")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem)
        self.label_14 = QtWidgets.QLabel(self.widget_12)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_187.addWidget(self.label_14)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem1)
        self.horizontalLayout_70 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_70.setObjectName("horizontalLayout_70")
        self.PyDMCheckbox_48 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_48.setToolTip("")
        self.PyDMCheckbox_48.setWhatsThis("")
        self.PyDMCheckbox_48.setObjectName("PyDMCheckbox_48")
        self.horizontalLayout_70.addWidget(self.PyDMCheckbox_48)
        self.PyDMLed_48 = PyDMLed(self.widget_12)
        self.PyDMLed_48.setToolTip("")
        self.PyDMLed_48.setWhatsThis("")
        self.PyDMLed_48.setObjectName("PyDMLed_48")
        self.horizontalLayout_70.addWidget(self.PyDMLed_48)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_70)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem2)
        self.horizontalLayout_69 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_69.setObjectName("horizontalLayout_69")
        self.PyDMCheckbox_47 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_47.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PyDMCheckbox_47.sizePolicy().hasHeightForWidth())
        self.PyDMCheckbox_47.setSizePolicy(sizePolicy)
        self.PyDMCheckbox_47.setToolTip("")
        self.PyDMCheckbox_47.setWhatsThis("")
        self.PyDMCheckbox_47.setObjectName("PyDMCheckbox_47")
        self.horizontalLayout_69.addWidget(self.PyDMCheckbox_47)
        self.PyDMLed_47 = PyDMLed(self.widget_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PyDMLed_47.sizePolicy().hasHeightForWidth())
        self.PyDMLed_47.setSizePolicy(sizePolicy)
        self.PyDMLed_47.setToolTip("")
        self.PyDMLed_47.setWhatsThis("")
        self.PyDMLed_47.setObjectName("PyDMLed_47")
        self.horizontalLayout_69.addWidget(self.PyDMLed_47)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_69)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem3)
        self.horizontalLayout_68 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_68.setObjectName("horizontalLayout_68")
        self.PyDMCheckbox_46 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_46.setToolTip("")
        self.PyDMCheckbox_46.setWhatsThis("")
        self.PyDMCheckbox_46.setObjectName("PyDMCheckbox_46")
        self.horizontalLayout_68.addWidget(self.PyDMCheckbox_46)
        self.PyDMLed_46 = PyDMLed(self.widget_12)
        self.PyDMLed_46.setToolTip("")
        self.PyDMLed_46.setWhatsThis("")
        self.PyDMLed_46.setObjectName("PyDMLed_46")
        self.horizontalLayout_68.addWidget(self.PyDMLed_46)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_68)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem4)
        self.horizontalLayout_67 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_67.setObjectName("horizontalLayout_67")
        self.PyDMCheckbox_45 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_45.setToolTip("")
        self.PyDMCheckbox_45.setWhatsThis("")
        self.PyDMCheckbox_45.setObjectName("PyDMCheckbox_45")
        self.horizontalLayout_67.addWidget(self.PyDMCheckbox_45)
        self.PyDMLed_45 = PyDMLed(self.widget_12)
        self.PyDMLed_45.setToolTip("")
        self.PyDMLed_45.setWhatsThis("")
        self.PyDMLed_45.setObjectName("PyDMLed_45")
        self.horizontalLayout_67.addWidget(self.PyDMLed_45)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_67)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem5)
        self.horizontalLayout_66 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_66.setObjectName("horizontalLayout_66")
        self.PyDMCheckbox_44 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_44.setToolTip("")
        self.PyDMCheckbox_44.setWhatsThis("")
        self.PyDMCheckbox_44.setObjectName("PyDMCheckbox_44")
        self.horizontalLayout_66.addWidget(self.PyDMCheckbox_44)
        self.PyDMLed_44 = PyDMLed(self.widget_12)
        self.PyDMLed_44.setToolTip("")
        self.PyDMLed_44.setWhatsThis("")
        self.PyDMLed_44.setObjectName("PyDMLed_44")
        self.horizontalLayout_66.addWidget(self.PyDMLed_44)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_66)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem6)
        self.horizontalLayout_65 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_65.setObjectName("horizontalLayout_65")
        self.PyDMCheckbox_43 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_43.setToolTip("")
        self.PyDMCheckbox_43.setWhatsThis("")
        self.PyDMCheckbox_43.setObjectName("PyDMCheckbox_43")
        self.horizontalLayout_65.addWidget(self.PyDMCheckbox_43)
        self.PyDMLed_43 = PyDMLed(self.widget_12)
        self.PyDMLed_43.setToolTip("")
        self.PyDMLed_43.setWhatsThis("")
        self.PyDMLed_43.setObjectName("PyDMLed_43")
        self.horizontalLayout_65.addWidget(self.PyDMLed_43)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_65)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem7)
        self.horizontalLayout_64 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_64.setObjectName("horizontalLayout_64")
        self.PyDMCheckbox_42 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_42.setToolTip("")
        self.PyDMCheckbox_42.setWhatsThis("")
        self.PyDMCheckbox_42.setObjectName("PyDMCheckbox_42")
        self.horizontalLayout_64.addWidget(self.PyDMCheckbox_42)
        self.PyDMLed_42 = PyDMLed(self.widget_12)
        self.PyDMLed_42.setToolTip("")
        self.PyDMLed_42.setWhatsThis("")
        self.PyDMLed_42.setObjectName("PyDMLed_42")
        self.horizontalLayout_64.addWidget(self.PyDMLed_42)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_64)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem8)
        self.horizontalLayout_63 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_63.setObjectName("horizontalLayout_63")
        self.PyDMCheckbox_41 = PyDMCheckbox(self.widget_12)
        self.PyDMCheckbox_41.setToolTip("")
        self.PyDMCheckbox_41.setWhatsThis("")
        self.PyDMCheckbox_41.setObjectName("PyDMCheckbox_41")
        self.horizontalLayout_63.addWidget(self.PyDMCheckbox_41)
        self.PyDMLed_41 = PyDMLed(self.widget_12)
        self.PyDMLed_41.setToolTip("")
        self.PyDMLed_41.setWhatsThis("")
        self.PyDMLed_41.setObjectName("PyDMLed_41")
        self.horizontalLayout_63.addWidget(self.PyDMLed_41)
        self.horizontalLayout_187.addLayout(self.horizontalLayout_63)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_187.addItem(spacerItem9)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_14.setText(_translate("Form", "Section 20"))

from pydm.widgets.checkbox import PyDMCheckbox
from pydm.widgets.led import PyDMLed
