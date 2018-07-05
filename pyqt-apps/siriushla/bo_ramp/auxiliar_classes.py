"""Booster Ramp Control HLA: Auxiliar Classes Module."""

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QScrollArea, QAbstractItemView, \
                            QVBoxLayout, QGridLayout, QLineEdit, \
                            QPushButton, QTableWidget, QTableWidgetItem, \
                            QRadioButton, QFormLayout, QDoubleSpinBox, \
                            QComboBox, QSpinBox, QStyledItemDelegate, \
                            QSpacerItem, QSizePolicy as QSzPlcy
from siriushla.widgets.windows import SiriusDialog
from siriuspy.servconf.conf_service import ConfigService as _ConfigService
from siriuspy.ramp import ramp


class InsertNormalizedConfig(SiriusDialog):
    """Auxiliar window to insert a new normalized config."""

    insertConfig = pyqtSignal(list)

    def __init__(self, parent):
        """Initialize object."""
        super().__init__(parent)
        self.normalized_config = ramp.BoosterNormalized()
        self.setWindowTitle('Insert Normalized Configuration')
        self._setupUi()

    def _setupUi(self):
        vlay = QVBoxLayout()
        vlay.addWidget(
            QLabel('<h4>Insert a Normalized Configuration</h4>', self),
            alignment=Qt.AlignCenter)

        self.rb_interp = QRadioButton('By interpolation')
        self.rb_confsrv = QRadioButton(
            'By taking an existing one from Config Server')
        self.rb_create = QRadioButton('By creating a new configuration')
        self.config_data = QWidget()
        self._setupConfigDataWidget()

        self.rb_interp.toggled.connect(self.interp_settings.setVisible)
        self.rb_interp.setChecked(True)
        self.rb_confsrv.toggled.connect(self.confsrv_settings.setVisible)
        self.rb_create.toggled.connect(self.create_settings.setVisible)

        vlay.addSpacerItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))
        vlay.addWidget(self.rb_interp)
        vlay.addWidget(self.rb_confsrv)
        vlay.addWidget(self.rb_create)
        vlay.addSpacerItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum))
        vlay.addWidget(self.config_data)

        self.setLayout(vlay)

    def _setupConfigDataWidget(self):
        vlay = QVBoxLayout()
        self.interp_settings = QWidget()
        self.confsrv_settings = QWidget()
        self.create_settings = QWidget()
        self.confsrv_settings.setVisible(False)
        self.create_settings.setVisible(False)
        vlay.addWidget(self.interp_settings)
        vlay.addWidget(self.confsrv_settings)
        vlay.addWidget(self.create_settings)
        self.config_data.setLayout(vlay)
        self.interp_settings.setFixedSize(600, 750)
        self.confsrv_settings.setFixedSize(600, 750)
        self.create_settings.setFixedSize(600, 750)

        flay_interp = QFormLayout()
        flay_interp.setLabelAlignment(Qt.AlignRight)
        self.le_interp_name = QLineEdit(self)
        self.sb_interp_time = QDoubleSpinBox(self)
        self.sb_interp_time.setMaximum(490)
        self.sb_interp_time.setDecimals(6)
        self.bt_interp = QPushButton('Insert', self)
        self.bt_interp.clicked.connect(self._emitInsertConfigData)
        flay_interp.addRow(QLabel('Name: ', self), self.le_interp_name)
        flay_interp.addRow(QLabel('Time: ', self), self.sb_interp_time)
        flay_interp.addRow(self.bt_interp)

        flay_confsrv = QFormLayout()
        flay_confsrv.setLabelAlignment(Qt.AlignRight)
        self.cb_confsrv_name = QComboBox(self)
        self.cb_confsrv_name.setStyleSheet(
            """ QComboBox::item {
                    height: 30px;}
            """)
        metadata = self.normalized_config.configsrv_find()
        for data in metadata:
            self.cb_confsrv_name.addItem(data['name'])
        self.sb_confsrv_time = QDoubleSpinBox(self)
        self.sb_confsrv_time.setMaximum(490)
        self.sb_confsrv_time.setDecimals(6)
        self.bt_confsrv = QPushButton('Insert', self)
        self.bt_confsrv.clicked.connect(self._emitInsertConfigData)
        flay_confsrv.addRow(QLabel('Name: ', self), self.cb_confsrv_name)
        flay_confsrv.addRow(QLabel('Time: ', self), self.sb_confsrv_time)
        flay_confsrv.addRow(self.bt_confsrv)

        flay_create = QFormLayout()
        self.le_create_name = QLineEdit(self)
        scrollarea = QScrollArea()
        scrollarea.setMinimumWidth(590)
        self.data = QWidget()
        flay_configdata = QFormLayout()
        flay_configdata.setLabelAlignment(Qt.AlignRight)
        config_template = self.normalized_config.get_config_type_template()
        for ma in config_template.keys():
            ma_value = QDoubleSpinBox(self.data)
            ma_value.setObjectName(ma)
            ma_value.setDecimals(6)
            flay_configdata.addRow(QLabel(ma + ': ', self), ma_value)
        self.data.setLayout(flay_configdata)
        scrollarea.setWidget(self.data)
        self.sb_create_time = QDoubleSpinBox(self)
        self.sb_create_time.setDecimals(6)
        self.sb_create_time.setMaximum(490)
        self.bt_create = QPushButton('Insert', self)
        self.bt_create.clicked.connect(self._emitInsertConfigData)
        flay_create.addRow(QLabel('Name: ', self), self.le_create_name)
        flay_create.addRow(scrollarea)
        flay_create.addRow(QLabel('Time: ', self), self.sb_create_time)
        flay_create.addRow(self.bt_create)

        self.interp_settings.setLayout(flay_interp)
        self.confsrv_settings.setLayout(flay_confsrv)
        self.create_settings.setLayout(flay_create)

    def _emitInsertConfigData(self):
        sender = self.sender()
        data = list()
        if sender is self.bt_interp:
            time = self.sb_interp_time.value()
            name = self.le_interp_name.text()
            nconfig = None
            option = 0
        elif sender is self.bt_confsrv:
            time = self.sb_confsrv_time.value()
            name = self.cb_confsrv_name.currentText()
            nconfig = None
            option = 1
        elif sender is self.bt_create:
            time = self.sb_create_time.value()
            name = self.le_create_name.text()
            config_template = self.normalized_config.get_config_type_template()
            nconfig = dict()
            for ma in config_template.keys():
                w = self.data.findChild(QDoubleSpinBox, name=ma)
                nconfig[ma] = w.value()
            option = 2
        data = [time, name, nconfig, option]
        self.insertConfig.emit(data)
        self.close()


class DeleteNormalizedConfig(SiriusDialog):
    """Auxiliar window to delete a normalized config."""

    deleteConfig = pyqtSignal(str)

    def __init__(self, parent, table_map):
        """Initialize object."""
        super().__init__(parent)
        self.normalized_config = ramp.BoosterNormalized()
        self.setWindowTitle('Delete Normalized Configuration')
        self.table_map = table_map
        self._setupUi()

    def _setupUi(self):
        glay = QGridLayout()
        label = QLabel('<h4>Delete a Normalized Configuration</h4>', self)
        label.setAlignment(Qt.AlignCenter)
        glay.addWidget(label, 0, 0, 1, 2)

        self.sb_confignumber = QSpinBox(self)
        self.sb_confignumber.setMinimum(1)
        self.sb_confignumber.setMaximum(max(self.table_map['rows'].values())+1)
        self.sb_confignumber.setMaximumWidth(150)
        self.sb_confignumber.valueChanged.connect(self._searchConfigByIndex)
        self.bt_delete = QPushButton('Delete', self)
        self.bt_delete.clicked.connect(self._emitDeleteConfigData)
        for key, value in self.table_map['rows'].items():
            if value == 0:
                label = key
                self.l_configname = QLabel(label, self)
                self.l_configname.setSizePolicy(QSzPlcy.MinimumExpanding,
                                                QSzPlcy.Preferred)
                if label in ['Injection', 'Ejection']:
                    self.bt_delete.setEnabled(False)
                else:
                    self.bt_delete.setEnabled(True)
                break

        glay.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 1, 0)
        glay.addWidget(self.sb_confignumber, 2, 0)
        glay.addWidget(self.l_configname, 2, 1)
        glay.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 3, 0)
        glay.addWidget(self.bt_delete, 4, 0, 1, 2)

        self.setLayout(glay)

    @pyqtSlot(int)
    def _searchConfigByIndex(self, config_idx):
        for label, value in self.table_map['rows'].items():
            if config_idx == (value + 1):
                self.l_configname.setText(label)
                if label in ['Injection', 'Ejection']:
                    self.bt_delete.setEnabled(False)
                else:
                    self.bt_delete.setEnabled(True)
                break

    def _emitDeleteConfigData(self):
        self.deleteConfig.emit(self.l_configname.text())
        self.close()


class EditNormalizedConfig(SiriusDialog):
    """Auxiliar window to edit an existing normalized config."""

    editConfig = pyqtSignal(dict)

    def __init__(self, parent, norm_config):
        """Initialize object."""
        super().__init__(parent)
        self.norm_config = norm_config
        self.setWindowTitle('Edit Normalized Configuration')
        self._setupUi()

    def _setupUi(self):
        glay = QGridLayout()
        label = QLabel(self.norm_config.name, self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""font-weight: bold;""")

        scrollarea = QScrollArea()
        scrollarea.setMinimumWidth(500)
        self.data = QWidget()
        flay_configdata = QFormLayout()
        flay_configdata.setLabelAlignment(Qt.AlignRight)
        config_template = self.norm_config.get_config_type_template()
        self.norm_config.configsrv_load()
        for ma in config_template.keys():
            ma_value = QDoubleSpinBox(self.data)
            ma_value.setDecimals(6)
            ma_value.setValue(self.norm_config[ma])
            ma_value.setObjectName(ma)
            flay_configdata.addRow(QLabel(ma + ': ', self), ma_value)
        self.data.setLayout(flay_configdata)
        scrollarea.setWidget(self.data)

        self.bt_apply = QPushButton('Apply Changes', self)
        self.bt_apply.clicked.connect(self._emitConfigChanges)
        self.bt_cancel = QPushButton('Cancel', self)
        self.bt_cancel.clicked.connect(self.close)

        glay.addWidget(label, 0, 0, 1, 2)
        glay.addWidget(scrollarea, 1, 0, 1, 2)
        glay.addWidget(self.bt_apply, 2, 0)
        glay.addWidget(self.bt_cancel, 2, 1)

        self.setLayout(glay)

    def _emitConfigChanges(self):
        config_template = self.norm_config.get_config_type_template()
        nconfig = dict()
        for ma in config_template.keys():
            w = self.data.findChild(QDoubleSpinBox, name=ma)
            nconfig[ma] = w.value()
        self.editConfig.emit(nconfig)
        self.close()


class OpticsAdjustSettings(SiriusDialog):
    """Auxiliar window to optics adjust settings."""

    updateSettings = pyqtSignal(list)

    def __init__(self, parent, tuneconfig_currname, chromconfig_currname):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Optics Adjust Settings')
        self.tuneconfig_currname = tuneconfig_currname
        self.chromconfig_currname = chromconfig_currname
        self.cs = _ConfigService()
        self._setupUi()

    def _setupUi(self):
        self.setFixedWidth(708)
        lay = QVBoxLayout()

        self._setupTuneSettings()
        self._setupChromSettings()
        # TODO: insert orbit correction settings
        self.bt_apply = QPushButton('Apply Settings', self)
        self.bt_apply.clicked.connect(self._emitSettings)

        lay.addItem(QSpacerItem(20, 60, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.addLayout(self.lay_tune_settings)
        lay.addItem(QSpacerItem(20, 60, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.addLayout(self.lay_chrom_settings)
        lay.addItem(QSpacerItem(20, 60, QSzPlcy.Fixed, QSzPlcy.Fixed))
        lay.addWidget(self.bt_apply)

        self.setLayout(lay)

    def _setupTuneSettings(self):
        lay = QVBoxLayout()

        l_tuneconfig = QLabel('<h3>Tune Variation Config</h3>', self)
        l_tuneconfig.setAlignment(Qt.AlignCenter)
        self.cb_tuneconfig = QComboBox(self)
        self.cb_tuneconfig.currentTextChanged.connect(self._showTuneConfigData)

        label_tunemat = QLabel('<h4>Matrix</h4>', self)
        label_tunemat.setAlignment(Qt.AlignCenter)
        self.table_tunemat = QTableWidget(self)
        self.table_tunemat.setFixedHeight(135)
        self.table_tunemat.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_tunemat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_tunemat.setRowCount(2)
        self.table_tunemat.setColumnCount(2)
        self.table_tunemat.setVerticalHeaderLabels(['  X', '  Y'])
        self.table_tunemat.setHorizontalHeaderLabels(['QF', 'QD'])
        self.table_tunemat.horizontalHeader().setDefaultSectionSize(320)
        self.table_tunemat.verticalHeader().setDefaultSectionSize(48)

        label_nomKL = QLabel('<h4>Nominal KL</h4>')
        label_nomKL.setAlignment(Qt.AlignCenter)
        self.table_nomKL = QTableWidget(self)
        self.table_nomKL.setFixedHeight(85)
        self.table_nomKL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_nomKL.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_nomKL.setRowCount(1)
        self.table_nomKL.setColumnCount(2)
        self.table_nomKL.setVerticalHeaderLabels(['KL'])
        self.table_nomKL.setHorizontalHeaderLabels(['QF', 'QD'])
        self.table_nomKL.horizontalHeader().setDefaultSectionSize(320)
        self.table_nomKL.verticalHeader().setDefaultSectionSize(48)

        querry = self.cs.find_configs(config_type='bo_tunecorr_params')
        for c in querry['result']:
            self.cb_tuneconfig.addItem(c['name'])
        self.cb_tuneconfig.setCurrentText(self.tuneconfig_currname)
        self._showTuneConfigData(self.tuneconfig_currname)

        lay.addWidget(l_tuneconfig)
        lay.addWidget(self.cb_tuneconfig)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Fixed))
        lay.addWidget(label_tunemat)
        lay.addWidget(self.table_tunemat)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Fixed))
        lay.addWidget(label_nomKL)
        lay.addWidget(self.table_nomKL)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Fixed))

        self.lay_tune_settings = lay

    def _setupChromSettings(self):
        lay = QVBoxLayout()

        l_chromconfig = QLabel('<h3>Chromaticity Variation Config</h3>', self)
        l_chromconfig.setAlignment(Qt.AlignCenter)
        self.cb_chromconfig = QComboBox(self)
        self.cb_chromconfig.currentTextChanged.connect(
            self._showChromConfigData)

        l_chrommat = QLabel('<h4>Matrix</h4>', self)
        l_chrommat.setAlignment(Qt.AlignCenter)
        self.table_chrommat = QTableWidget(self)
        self.table_chrommat.setFixedHeight(135)
        self.table_chrommat.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_chrommat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_chrommat.setRowCount(2)
        self.table_chrommat.setColumnCount(2)
        self.table_chrommat.setVerticalHeaderLabels(['  X', '  Y'])
        self.table_chrommat.setHorizontalHeaderLabels(['SF', 'SD'])
        self.table_chrommat.horizontalHeader().setDefaultSectionSize(320)
        self.table_chrommat.verticalHeader().setDefaultSectionSize(48)

        l_nomSL = QLabel('<h4>Nominal SL</h4>')
        l_nomSL.setAlignment(Qt.AlignCenter)
        self.table_nomSL = QTableWidget(self)
        self.table_nomSL.setFixedHeight(85)
        self.table_nomSL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_nomSL.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_nomSL.setRowCount(1)
        self.table_nomSL.setColumnCount(2)
        self.table_nomSL.setVerticalHeaderLabels(['SL'])
        self.table_nomSL.setHorizontalHeaderLabels(['SF', 'SD'])
        self.table_nomSL.horizontalHeader().setDefaultSectionSize(320)
        self.table_nomSL.verticalHeader().setDefaultSectionSize(48)

        l_nomchrom = QLabel('<h4>Nominal Chrom</h4>')
        l_nomchrom.setAlignment(Qt.AlignCenter)
        self.label_nomchrom = QLabel()
        self.label_nomchrom.setMinimumHeight(48)
        self.label_nomchrom.setAlignment(Qt.AlignCenter)

        querry = self.cs.find_configs(config_type='bo_chromcorr_params')
        for c in querry['result']:
            self.cb_chromconfig.addItem(c['name'])
        self.cb_chromconfig.setCurrentText(self.chromconfig_currname)
        self._showChromConfigData(self.chromconfig_currname)

        lay.addWidget(l_chromconfig)
        lay.addWidget(self.cb_chromconfig)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Fixed))
        lay.addWidget(l_chrommat)
        lay.addWidget(self.table_chrommat)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Fixed))
        lay.addWidget(l_nomSL)
        lay.addWidget(self.table_nomSL)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Minimum, QSzPlcy.Fixed))
        lay.addWidget(l_nomchrom)
        lay.addWidget(self.label_nomchrom)
        self.lay_chrom_settings = lay

    @pyqtSlot(str)
    def _showTuneConfigData(self, tuneconfig_currname):
        querry = self.cs.get_config(config_type='bo_tunecorr_params',
                                    name=tuneconfig_currname)
        mat = querry['result']['value']['matrix']
        self.table_tunemat.setItem(0, 0, QTableWidgetItem(str(mat[0][0])))
        self.table_tunemat.setItem(0, 1, QTableWidgetItem(str(mat[0][1])))
        self.table_tunemat.setItem(1, 0, QTableWidgetItem(str(mat[1][0])))
        self.table_tunemat.setItem(1, 1, QTableWidgetItem(str(mat[1][1])))
        nomKL = querry['result']['value']['nominal KLs']
        self.table_nomKL.setItem(0, 0, QTableWidgetItem(str(nomKL[0])))
        self.table_nomKL.setItem(0, 1, QTableWidgetItem(str(nomKL[1])))

    @pyqtSlot(str)
    def _showChromConfigData(self, chromconfig_currname):
        querry = self.cs.get_config(config_type='bo_chromcorr_params',
                                    name=chromconfig_currname)
        mat = querry['result']['value']['matrix']
        self.table_chrommat.setItem(0, 0, QTableWidgetItem(str(mat[0][0])))
        self.table_chrommat.setItem(0, 1, QTableWidgetItem(str(mat[0][1])))
        self.table_chrommat.setItem(1, 0, QTableWidgetItem(str(mat[1][0])))
        self.table_chrommat.setItem(1, 1, QTableWidgetItem(str(mat[1][1])))
        nomSL = querry['result']['value']['nominal SLs']
        self.table_nomSL.setItem(0, 0, QTableWidgetItem(str(nomSL[0])))
        self.table_nomSL.setItem(0, 1, QTableWidgetItem(str(nomSL[1])))
        self.label_nomchrom.setText(
            str(querry['result']['value']['nominal chrom']))

    def _emitSettings(self):
        tuneconfig_name = self.cb_tuneconfig.currentText()
        chromconfig_name = self.cb_chromconfig.currentText()
        self.updateSettings.emit([tuneconfig_name, chromconfig_name])
        self.close()


class SpinBoxDelegate(QStyledItemDelegate):
    """Auxiliar class to draw a SpinBox in table items on editing."""

    def createEditor(self, parent, option, index):
        """Create editor."""
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(500)
        editor.setDecimals(4)
        return editor

    def setEditorData(self, spinBox, index):
        """Set editor data."""
        value = index.model().data(index, Qt.EditRole)
        spinBox.setValue(float(value))

    def setModelData(self, spinBox, model, index):
        """Set model data."""
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, spinBox, option, index):
        """Update editor geometry."""
        spinBox.setGeometry(option.rect)


class MessageBox(SiriusDialog):
    """Auxiliar dialog to inform user about errors and pendencies."""

    acceptedSignal = pyqtSignal()
    regectedSignal = pyqtSignal()

    def __init__(self, parent=None, title='', message='',
                 accept_button_text='', regect_button_text=''):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.message = message
        self.accept_button_text = accept_button_text
        self.regect_button_text = regect_button_text
        self._setupUi()

    def _setupUi(self):
        glay = QGridLayout()

        self.label = QLabel(self.message, self)
        glay.addWidget(self.label, 0, 0, 1, 3)

        self.accept_button = QPushButton(self.accept_button_text, self)
        self.accept_button.clicked.connect(self._emitAccepted)
        glay.addWidget(self.accept_button, 1, 1)

        if self.regect_button_text != '':
            self.regect_button = QPushButton(self.regect_button_text, self)
            self.regect_button.clicked.connect(self._emitRegected)
            glay.addWidget(self.regect_button, 1, 2)

        self.setLayout(glay)

    def _emitAccepted(self):
        self.acceptedSignal.emit()
        self.close()

    def _emitRegected(self):
        self.regectedSignal.emit()
        self.close()


class CustomTableWidgetItem(QTableWidgetItem):
    """Auxiliar class to make a table column sortable by numeric data."""

    def __init__(self, value):
        """Initialize object."""
        super().__init__('{}'.format(value))

    def __lt__(self, other):
        """Change default sort method to sort by numeric data."""
        if isinstance(other, CustomTableWidgetItem):
            selfDataValue = float(self.data(Qt.EditRole))
            otherDataValue = float(other.data(Qt.EditRole))
            return selfDataValue < otherDataValue
        else:
            return QTableWidgetItem.__lt__(self, other)
