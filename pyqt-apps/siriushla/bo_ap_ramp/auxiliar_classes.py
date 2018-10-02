"""Booster Ramp Control HLA: Auxiliar Classes Module."""

from qtpy.QtCore import Qt, Signal, Slot, QStringListModel, QLocale
from qtpy.QtWidgets import QLabel, QWidget, QScrollArea, QAbstractItemView, \
                           QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, \
                           QPushButton, QTableWidget, QTableWidgetItem, \
                           QRadioButton, QFormLayout, QDoubleSpinBox, \
                           QComboBox, QSpinBox, QStyledItemDelegate, \
                           QSpacerItem, QSizePolicy as QSzPlcy, QCheckBox, \
                           QTabWidget, QCompleter
from pydm.widgets import PyDMLabel, PyDMSpinbox
from siriushla.widgets.windows import SiriusDialog
from siriuspy.servconf.conf_service import ConfigService as _ConfigService
from siriuspy.servconf.util import \
    generate_config_name as _generate_config_name
from siriuspy.ramp import ramp


class LoadRampConfig(SiriusDialog):
    """Auxiliar window to get a ramp config name to load."""

    newConfigNameSignal = Signal(str)
    loadSignal = Signal()
    saveSignal = Signal()

    def __init__(self, parent, ramp_config):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Load ramp configuration from server')
        self.ramp_config = ramp_config
        self._setupUi()

    def _setupUi(self):
        l_insert = QLabel('Insert a configuration name: ', self,
                          alignment=Qt.AlignCenter)
        l_insert.setFixedHeight(40)

        completer = QCompleter()
        self._completer_model = QStringListModel()
        completer.setModel(self._completer_model)
        allconfigs = _ConfigService().find_configs(config_type='bo_ramp')
        string_list = list()
        for c in allconfigs['result']:
            string_list.append(c['name'])
        self._completer_model.setStringList(string_list)

        if self.ramp_config is not None:
            le_text = self.ramp_config.name
        else:
            le_text = ''
        self.le_config = QLineEdit(le_text, self)
        self.le_config.setCompleter(completer)
        self.le_config.editingFinished.connect(self._configNameChanged)

        self.bt_load = QPushButton('Load', self)
        self.bt_load.setFixedWidth(140)
        self.bt_load.setEnabled(False)
        self.bt_load.setAutoDefault(False)
        self.bt_load.setDefault(False)
        self.bt_load.clicked.connect(self._load)

        self.bt_cancel = QPushButton('Cancel', self)
        self.bt_cancel.setFixedWidth(140)
        self.bt_cancel.setAutoDefault(False)
        self.bt_cancel.setDefault(False)
        self.bt_cancel.clicked.connect(self.close)

        self.l_warn = QLabel('', self)
        self.l_warn.setStyleSheet('color: red;')
        self.l_warn.setFixedWidth(750)

        lay = QGridLayout(self)
        lay.addWidget(l_insert, 0, 0)
        lay.addWidget(self.le_config, 1, 0)
        lay.addWidget(self.bt_load, 1, 1)
        lay.addWidget(self.l_warn, 2, 0)
        lay.addWidget(self.bt_cancel, 2, 1)

    def _configNameChanged(self):
        self.le_config.blockSignals(True)
        # the previous line fix a qt bug that triggered lineedit.editFinished
        # to be called twice when enter key is pressed
        name = self.le_config.text()
        if name != '' and ramp.BoosterRamp(name).configsrv_exist():
            self.l_warn.setText('')
            self.bt_load.setEnabled(True)
        else:
            if name == '':
                self.l_warn.setText('Insert a config name!')
            elif not ramp.BoosterRamp(name).configsrv_exist():
                self.l_warn.setText('There is no config with this name!')
            self.bt_load.setEnabled(False)
        self.le_config.blockSignals(False)

    def _load(self):
        name = self.le_config.text()
        if self.ramp_config is not None:
            if not self.ramp_config.configsrv_synchronized:
                save_changes = MessageBox(
                    self, 'Save changes?',
                    'There are unsaved changes. \n'
                    'Do you want to save?'.format(name),
                    'Yes', 'Cancel')
                save_changes.acceptedSignal.connect(self._saveChanges)
                save_changes.exec_()

            if name != self.ramp_config.name:
                self.newConfigNameSignal.emit(name)
            else:
                self.ramp_config.configsrv_load()
                self.loadSignal.emit()
        else:
            self.newConfigNameSignal.emit(name)
        self.close()

    def _saveChanges(self):
        self.saveSignal.emit()


class NewRampConfigGetName(SiriusDialog):
    """Auxiliar window to get a configuration name to create a new one."""

    newConfigNameSignal = Signal(str)
    saveSignal = Signal()

    def __init__(self, parent, config, config_type, new_from_template=True):
        """Initialize object."""
        super().__init__(parent)
        self.config = config
        self.config_type = config_type
        self._new_from_template = new_from_template
        if new_from_template:
            self.setWindowTitle('New config from template')
        else:
            self.setWindowTitle('Save current config as...')
        self._setupUi()

    def _setupUi(self):
        l_insert = QLabel('Insert a new configuration name: ', self,
                          alignment=Qt.AlignCenter)
        l_insert.setFixedHeight(40)

        self.le_config = QLineEdit('', self)
        self.le_config.setText(_generate_config_name())
        self.le_config.editingFinished.connect(self._configNameChanged)

        self.bt_create = QPushButton('Create', self)
        self.bt_create.setFixedWidth(140)
        self.bt_create.setEnabled(False)
        self.bt_create.setAutoDefault(False)
        self.bt_create.setDefault(False)
        self.bt_create.clicked.connect(self._create)

        self.l_warn = QLabel('', self)
        self.l_warn.setStyleSheet('color: red;')
        self.l_warn.setFixedWidth(750)

        self.bt_cancel = QPushButton('Cancel', self)
        self.bt_cancel.setFixedWidth(140)
        self.bt_cancel.setAutoDefault(False)
        self.bt_cancel.setDefault(False)
        self.bt_cancel.clicked.connect(self.close)

        lay = QGridLayout(self)
        lay.addWidget(l_insert, 0, 0)
        lay.addWidget(self.le_config, 1, 0)
        lay.addWidget(self.bt_create, 1, 1)
        lay.addWidget(self.l_warn, 2, 0)
        lay.addWidget(self.bt_cancel, 2, 1)

    def _configNameChanged(self):
        self.le_config.blockSignals(True)
        # the previous line fix a qt bug that triggered lineedit.editFinished
        # to be called twice when enter key is pressed

        name = self.le_config.text()
        if name != '' and not self.config_type(name).configsrv_exist():
            self.bt_create.setEnabled(True)
            self.l_warn.setText('')
        else:
            if name == '':
                self.l_warn.setText('Insert a config name!')
            elif self.config_type(name).configsrv_exist():
                self.l_warn.setText('A configuration with this '
                                    'name already exists!')
            self.bt_create.setEnabled(False)
        self.le_config.blockSignals(False)

    def _create(self):
        name = self.le_config.text()
        if (self._new_from_template and (self.config is not None)):
            if not self.config.configsrv_synchronized:
                save_changes = MessageBox(
                    self, 'Save changes?',
                    'There are unsaved changes. \n'
                    'Do you want to save?'.format(name),
                    'Yes', 'Cancel')
                save_changes.acceptedSignal.connect(self._saveChanges)
                save_changes.exec_()
            else:
                self.newConfigNameSignal.emit(name)
                self.close()
        else:
            self.newConfigNameSignal.emit(name)
            self.close()

    def _saveChanges(self):
        self.saveSignal.emit()


class InsertNormalizedConfig(SiriusDialog):
    """Auxiliar window to insert a new normalized config."""

    insertConfig = Signal(list)

    def __init__(self, parent):
        """Initialize object."""
        super().__init__(parent)
        self.normalized_config = ramp.BoosterNormalized()
        self.setWindowTitle('Insert Normalized Configuration')
        self._setupUi()

    def _setupUi(self):
        self.rb_interp = QRadioButton('By interpolation')
        self.rb_confsrv = QRadioButton(
            'By taking an existing one from Config Server')
        self.rb_create = QRadioButton(
            'By creating a new nominal configuration')
        self.config_data = QWidget()
        self._setupConfigDataWidget()

        self.rb_interp.toggled.connect(self.interp_settings.setVisible)
        self.rb_interp.setChecked(True)
        self.rb_confsrv.toggled.connect(self.confsrv_settings.setVisible)
        self.rb_create.toggled.connect(self.create_settings.setVisible)

        vlay = QVBoxLayout()
        vlay.addItem(QSpacerItem(40, 20, QSzPlcy.Fixed, QSzPlcy.Expanding))
        vlay.addWidget(
            QLabel('<h4>Insert a Normalized Configuration</h4>', self),
            alignment=Qt.AlignCenter)
        vlay.addItem(QSpacerItem(40, 20, QSzPlcy.Fixed, QSzPlcy.Expanding))
        vlay.addWidget(self.rb_interp)
        vlay.addWidget(self.rb_confsrv)
        vlay.addWidget(self.rb_create)
        vlay.addItem(QSpacerItem(40, 20, QSzPlcy.Fixed, QSzPlcy.Expanding))
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
        self.interp_settings.setFixedSize(600, 160)
        self.confsrv_settings.setFixedSize(600, 160)
        self.create_settings.setFixedSize(600, 160)

        # to insert interpolating existing norm configs
        flay_interp = QFormLayout()
        self.le_interp_name = QLineEdit(self)
        self.le_interp_name.setText(_generate_config_name())
        self.sb_interp_time = QDoubleSpinBox(self)
        self.sb_interp_time.setMaximum(490)
        self.sb_interp_time.setDecimals(6)
        self.bt_interp = QPushButton('Insert', self)
        self.bt_interp.setAutoDefault(False)
        self.bt_interp.setDefault(False)
        self.bt_interp.clicked.connect(self._emitInsertConfigData)
        flay_interp.addRow(QLabel('Name: ', self), self.le_interp_name)
        flay_interp.addRow(QLabel('Time: ', self), self.sb_interp_time)
        flay_interp.addRow(self.bt_interp)

        # to insert a new norm config from an existing one
        flay_confsrv = QFormLayout()
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
        self.bt_confsrv.setAutoDefault(False)
        self.bt_confsrv.setDefault(False)
        self.bt_confsrv.clicked.connect(self._emitInsertConfigData)
        flay_confsrv.addRow(QLabel('Name: ', self), self.cb_confsrv_name)
        flay_confsrv.addRow(QLabel('Time: ', self), self.sb_confsrv_time)
        flay_confsrv.addRow(self.bt_confsrv)

        # to insert a new norm config equal to template
        flay_create = QFormLayout()
        self.le_create_name = QLineEdit(self)
        self.le_create_name.setText(_generate_config_name())
        self.sb_create_time = QDoubleSpinBox(self)
        self.sb_create_time.setDecimals(6)
        self.sb_create_time.setMaximum(490)
        self.bt_create = QPushButton('Insert', self)
        self.bt_create.setAutoDefault(False)
        self.bt_create.setDefault(False)
        self.bt_create.clicked.connect(self._emitInsertConfigData)
        flay_create.addRow(QLabel('Name: ', self), self.le_create_name)
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
        elif sender is self.bt_confsrv:
            time = self.sb_confsrv_time.value()
            name = self.cb_confsrv_name.currentText()
            n = ramp.BoosterNormalized(name)
            n.configsrv_load()
            nconfig = n.configuration
        elif sender is self.bt_create:
            time = self.sb_create_time.value()
            name = self.le_create_name.text()
            nconfig = self.normalized_config.get_config_type_template()
        data = [time, name, nconfig]
        self.insertConfig.emit(data)
        self.close()


class DeleteNormalizedConfig(SiriusDialog):
    """Auxiliar window to delete a normalized config."""

    deleteConfig = Signal(str)

    def __init__(self, parent, table_map, selected_item):
        """Initialize object."""
        super().__init__(parent)
        self.normalized_config = ramp.BoosterNormalized()
        self.setWindowTitle('Delete Normalized Configuration')
        self.table_map = table_map
        self.selected_item = selected_item
        self._setupUi()

    def _setupUi(self):
        glay = QGridLayout()
        label = QLabel('<h4>Delete a Normalized Configuration</h4>', self)
        label.setAlignment(Qt.AlignCenter)
        glay.addWidget(label, 0, 0, 1, 2)

        self.sb_confignumber = QSpinBox(self)
        self.sb_confignumber.setMinimum(1)
        self.sb_confignumber.setMaximum(max(self.table_map['rows'].keys())+1)
        self.sb_confignumber.setMaximumWidth(150)
        self.sb_confignumber.valueChanged.connect(self._searchConfigByIndex)
        self.bt_delete = QPushButton('Delete', self)
        self.bt_delete.setAutoDefault(False)
        self.bt_delete.setDefault(False)
        self.bt_delete.clicked.connect(self._emitDeleteConfigData)
        self.l_configname = QLabel('', self)
        self.l_configname.setSizePolicy(QSzPlcy.MinimumExpanding,
                                        QSzPlcy.Preferred)
        if self.selected_item:
            row = self.selected_item[0].row()
        else:
            row = 0
        self.sb_confignumber.setValue(row+1)
        self._searchConfigByIndex(row+1)

        glay.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 1, 0)
        glay.addWidget(self.sb_confignumber, 2, 0)
        glay.addWidget(self.l_configname, 2, 1)
        glay.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Minimum), 3, 0)
        glay.addWidget(self.bt_delete, 4, 0, 1, 2)

        self.setLayout(glay)

    @Slot(int)
    def _searchConfigByIndex(self, config_idx):
        label = self.table_map['rows'][config_idx - 1]
        self.l_configname.setText(label)
        if label in ['Injection', 'Ejection']:
            self.bt_delete.setEnabled(False)
        else:
            self.bt_delete.setEnabled(True)

    def _emitDeleteConfigData(self):
        self.deleteConfig.emit(self.l_configname.text())
        self.close()


class EditNormalizedConfig(SiriusDialog):
    """Auxiliar window to edit an existing normalized config."""

    editConfig = Signal(dict)

    def __init__(self, parent, norm_config, energyGeV, aux_magnets):
        """Initialize object."""
        super().__init__(parent)
        self.norm_config = norm_config
        self.energy = energyGeV
        self._aux_magnets = aux_magnets
        self.setWindowTitle('Edit Normalized Configuration')
        self._setupUi()

    def _setupUi(self):
        glay = QGridLayout()
        label = QLabel(self.norm_config.name, self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""font-weight: bold;""")

        scrollarea = QScrollArea()
        scrollarea.setFixedWidth(500)
        self.data = QWidget()
        flay_configdata = QFormLayout()
        manames = self.norm_config.get_config_type_template().keys()
        for ma in manames:
            ma_value = MyDoubleSpinBox(self.data)
            ma_value.setDecimals(6)
            ma_value.setValue(self.norm_config[ma])
            ma_value.setObjectName(ma)
            ma_value.setFixedWidth(200)
            ma_value.setFocusPolicy(Qt.StrongFocus)

            aux = self._aux_magnets[ma]
            currs = (aux.current_min, aux.current_max)
            lims = aux.conv_current_2_strength(
                currents=currs, strengths_dipole=self.energy)
            ma_value.setMinimum(min(lims))
            ma_value.setMaximum(max(lims))

            flay_configdata.addRow(QLabel(ma + ': ', self), ma_value)
        self.data.setLayout(flay_configdata)
        scrollarea.setWidget(self.data)

        self.cb_checklims = QCheckBox('Set limits according to energy', self)
        self.cb_checklims.setChecked(True)
        self.cb_checklims.stateChanged.connect(self._handleStrengtsLimits)
        self.bt_apply = QPushButton('Apply Changes', self)
        self.bt_apply.setAutoDefault(False)
        self.bt_apply.setDefault(False)
        self.bt_apply.clicked.connect(self._emitConfigChanges)
        self.bt_cancel = QPushButton('Cancel', self)
        self.bt_cancel.setAutoDefault(False)
        self.bt_cancel.setDefault(False)
        self.bt_cancel.clicked.connect(self.close)

        glay.addWidget(label, 0, 0, 1, 2)
        glay.addWidget(scrollarea, 1, 0, 1, 2)
        glay.addWidget(self.cb_checklims, 2, 0, 1, 2)
        glay.addWidget(self.bt_apply, 3, 0)
        glay.addWidget(self.bt_cancel, 3, 1)

        self.setLayout(glay)

    def _handleStrengtsLimits(self, state):
        manames = self.norm_config.get_config_type_template().keys()
        if state:
            for ma in manames:
                ma_value = self.data.findChild(QDoubleSpinBox, name=ma)
                aux = self._aux_magnets[ma]
                currs = (aux.current_min, aux.current_max)
                lims = aux.conv_current_2_strength(
                    currents=currs, strengths_dipole=self.energy)
                ma_value.setMinimum(min(lims))
                ma_value.setMaximum(max(lims))
        else:
            for ma in manames:
                ma_value = self.data.findChild(QDoubleSpinBox, name=ma)
                ma_value.setMinimum(-100)
                ma_value.setMaximum(100)

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

    updateSettings = Signal(list)

    def __init__(self, parent, tuneconfig_currname, chromconfig_currname):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Optics Adjust Settings')
        self.tuneconfig_currname = tuneconfig_currname
        self.chromconfig_currname = chromconfig_currname
        self.cs = _ConfigService()
        self._setupUi()

    def _setupUi(self):
        self.tune_settings = QWidget(self)
        self.tune_settings.setLayout(self._setupTuneSettings())
        self.chrom_settings = QWidget(self)
        self.chrom_settings.setLayout(self._setupChromSettings())
        self.orbit_settings = QWidget(self)
        self.orbit_settings.setLayout(self._setupOrbitSettings())
        self.bt_apply = QPushButton('Apply Settings', self)
        self.bt_apply.setFixedWidth(250)
        self.bt_apply.clicked.connect(self._emitSettings)
        hlay_apply = QHBoxLayout()
        hlay_apply.addItem(
            QSpacerItem(20, 60, QSzPlcy.Expanding, QSzPlcy.Fixed))
        hlay_apply.addWidget(self.bt_apply)

        tabs = QTabWidget(self)
        tabs.addTab(self.orbit_settings, 'Orbit')
        tabs.addTab(self.tune_settings, 'Tune')
        tabs.addTab(self.chrom_settings, 'Chromaticity')

        lay = QVBoxLayout()
        lay.addWidget(tabs)
        lay.addLayout(hlay_apply)

        self.setLayout(lay)

    def _setupOrbitSettings(self):
        l_orbitsettings = QLabel('<h3>Orbit Correction Settings</h3>', self)
        l_orbitsettings.setAlignment(Qt.AlignCenter)

        # TODO: insert orbit correction settings

        lay = QVBoxLayout()
        lay.addWidget(l_orbitsettings)

        return lay

    def _setupTuneSettings(self):
        l_tuneconfig = QLabel('<h3>Tune Variation Config</h3>', self)
        l_tuneconfig.setAlignment(Qt.AlignCenter)
        self.cb_tuneconfig = QComboBox(self)
        self.cb_tuneconfig.currentTextChanged.connect(self._showTuneConfigData)

        label_tunemat = QLabel('<h4>Matrix</h4>', self)
        label_tunemat.setAlignment(Qt.AlignCenter)
        self.table_tunemat = QTableWidget(self)
        self.table_tunemat.setFixedSize(686, 130)
        self.table_tunemat.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_tunemat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_tunemat.setRowCount(2)
        self.table_tunemat.setColumnCount(2)
        self.table_tunemat.setVerticalHeaderLabels(['  X', '  Y'])
        self.table_tunemat.setHorizontalHeaderLabels(['QF', 'QD'])
        self.table_tunemat.horizontalHeader().setDefaultSectionSize(320)
        self.table_tunemat.verticalHeader().setDefaultSectionSize(48)
        self.table_tunemat.setStyleSheet("background-color: #efebe7;")

        label_nomKL = QLabel('<h4>Nominal KL</h4>')
        label_nomKL.setAlignment(Qt.AlignCenter)
        self.table_nomKL = QTableWidget(self)
        self.table_nomKL.setFixedSize(685, 85)
        self.table_nomKL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_nomKL.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_nomKL.setRowCount(1)
        self.table_nomKL.setColumnCount(2)
        self.table_nomKL.setVerticalHeaderLabels(['KL'])
        self.table_nomKL.setHorizontalHeaderLabels(['QF', 'QD'])
        self.table_nomKL.horizontalHeader().setDefaultSectionSize(320)
        self.table_nomKL.verticalHeader().setDefaultSectionSize(48)
        self.table_nomKL.setStyleSheet("background-color: #efebe7;")

        querry = self.cs.find_configs(config_type='bo_tunecorr_params')
        for c in querry['result']:
            self.cb_tuneconfig.addItem(c['name'])
        self.cb_tuneconfig.setCurrentText(self.tuneconfig_currname)
        self._showTuneConfigData(self.tuneconfig_currname)

        lay = QVBoxLayout()
        lay.addWidget(l_tuneconfig)
        lay.addWidget(self.cb_tuneconfig)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Fixed, QSzPlcy.Expanding))
        lay.addWidget(label_tunemat)
        lay.addWidget(self.table_tunemat)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Fixed, QSzPlcy.Expanding))
        lay.addWidget(label_nomKL)
        lay.addWidget(self.table_nomKL)
        lay.addItem(
            QSpacerItem(20, 101, QSzPlcy.Fixed, QSzPlcy.MinimumExpanding))

        return lay

    def _setupChromSettings(self):
        l_chromconfig = QLabel('<h3>Chromaticity Variation Config</h3>', self)
        l_chromconfig.setAlignment(Qt.AlignCenter)
        self.cb_chromconfig = QComboBox(self)
        self.cb_chromconfig.currentTextChanged.connect(
            self._showChromConfigData)

        l_chrommat = QLabel('<h4>Matrix</h4>', self)
        l_chrommat.setAlignment(Qt.AlignCenter)
        self.table_chrommat = QTableWidget(self)
        self.table_chrommat.setFixedSize(686, 130)
        self.table_chrommat.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_chrommat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_chrommat.setRowCount(2)
        self.table_chrommat.setColumnCount(2)
        self.table_chrommat.setVerticalHeaderLabels(['  X', '  Y'])
        self.table_chrommat.setHorizontalHeaderLabels(['SF', 'SD'])
        self.table_chrommat.horizontalHeader().setDefaultSectionSize(320)
        self.table_chrommat.verticalHeader().setDefaultSectionSize(48)
        self.table_chrommat.setStyleSheet("background-color: #efebe7;")

        l_nomSL = QLabel('<h4>Nominal SL</h4>')
        l_nomSL.setAlignment(Qt.AlignCenter)
        self.table_nomSL = QTableWidget(self)
        self.table_nomSL.setFixedSize(683, 85)
        self.table_nomSL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_nomSL.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_nomSL.setRowCount(1)
        self.table_nomSL.setColumnCount(2)
        self.table_nomSL.setVerticalHeaderLabels(['SL'])
        self.table_nomSL.setHorizontalHeaderLabels(['SF', 'SD'])
        self.table_nomSL.horizontalHeader().setDefaultSectionSize(320)
        self.table_nomSL.verticalHeader().setDefaultSectionSize(48)
        self.table_nomSL.setStyleSheet("background-color: #efebe7;")

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

        lay = QVBoxLayout()
        lay.addWidget(l_chromconfig)
        lay.addWidget(self.cb_chromconfig)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Fixed, QSzPlcy.Expanding))
        lay.addWidget(l_chrommat)
        lay.addWidget(self.table_chrommat)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Fixed, QSzPlcy.Expanding))
        lay.addWidget(l_nomSL)
        lay.addWidget(self.table_nomSL)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Fixed, QSzPlcy.Expanding))
        lay.addWidget(l_nomchrom)
        lay.addWidget(self.label_nomchrom)

        return lay

    @Slot(str)
    def _showTuneConfigData(self, tuneconfig_currname):
        querry = self.cs.get_config(config_type='bo_tunecorr_params',
                                    name=tuneconfig_currname)
        mat = querry['result']['value']['matrix']
        self.table_tunemat.setItem(0, 0, QTableWidgetItem(str(mat[0][0])))
        self.table_tunemat.setItem(0, 1, QTableWidgetItem(str(mat[0][1])))
        self.table_tunemat.setItem(1, 0, QTableWidgetItem(str(mat[1][0])))
        self.table_tunemat.setItem(1, 1, QTableWidgetItem(str(mat[1][1])))
        self.table_tunemat.item(0, 0).setFlags(Qt.ItemIsEnabled)
        self.table_tunemat.item(0, 1).setFlags(Qt.ItemIsEnabled)
        self.table_tunemat.item(1, 0).setFlags(Qt.ItemIsEnabled)
        self.table_tunemat.item(1, 1).setFlags(Qt.ItemIsEnabled)
        nomKL = querry['result']['value']['nominal KLs']
        self.table_nomKL.setItem(0, 0, QTableWidgetItem(str(nomKL[0])))
        self.table_nomKL.setItem(0, 1, QTableWidgetItem(str(nomKL[1])))
        self.table_nomKL.item(0, 0).setFlags(Qt.ItemIsEnabled)
        self.table_nomKL.item(0, 1).setFlags(Qt.ItemIsEnabled)

    @Slot(str)
    def _showChromConfigData(self, chromconfig_currname):
        querry = self.cs.get_config(config_type='bo_chromcorr_params',
                                    name=chromconfig_currname)
        mat = querry['result']['value']['matrix']
        self.table_chrommat.setItem(0, 0, QTableWidgetItem(str(mat[0][0])))
        self.table_chrommat.setItem(0, 1, QTableWidgetItem(str(mat[0][1])))
        self.table_chrommat.setItem(1, 0, QTableWidgetItem(str(mat[1][0])))
        self.table_chrommat.setItem(1, 1, QTableWidgetItem(str(mat[1][1])))
        self.table_chrommat.item(0, 0).setFlags(Qt.ItemIsEnabled)
        self.table_chrommat.item(0, 1).setFlags(Qt.ItemIsEnabled)
        self.table_chrommat.item(1, 0).setFlags(Qt.ItemIsEnabled)
        self.table_chrommat.item(1, 1).setFlags(Qt.ItemIsEnabled)
        nomSL = querry['result']['value']['nominal SLs']
        self.table_nomSL.setItem(0, 0, QTableWidgetItem(str(nomSL[0])))
        self.table_nomSL.setItem(0, 1, QTableWidgetItem(str(nomSL[1])))
        self.table_nomSL.item(0, 0).setFlags(Qt.ItemIsEnabled)
        self.table_nomSL.item(0, 1).setFlags(Qt.ItemIsEnabled)
        self.label_nomchrom.setText(
            str(querry['result']['value']['nominal chrom']))

    def _emitSettings(self):
        tuneconfig_name = self.cb_tuneconfig.currentText()
        chromconfig_name = self.cb_chromconfig.currentText()
        self.updateSettings.emit([tuneconfig_name, chromconfig_name])
        self.close()


class StatisticSettings(SiriusDialog):
    """Auxiliar window to statistics settings."""

    updateSettings = Signal(list)

    def __init__(self, parent, prefix, injcurr_idx, ejecurr_idx):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Statistics Settings')
        self.prefix = prefix
        self.injcurr_idx = injcurr_idx
        self.ejecurr_idx = ejecurr_idx
        self._setupUi()

    def _setupUi(self):
        l_dcctacq = QLabel('<h4>DCCT Acquisitions Settings</h4>', self,
                           alignment=Qt.AlignCenter)

        l_nracq = QLabel('# of Acquisitions: ', self, alignment=Qt.AlignRight)
        self.pydmspinbox_NrAcq = PyDMSpinbox(
            parent=self,
            init_channel='ca://'+self.prefix+'BO-35D:DI-DCCT:??????-SP')
        self.pydmspinbox_NrAcq.setFixedSize(220, 40)
        self.pydmspinbox_NrAcq.setAlignment(Qt.AlignCenter)
        self.pydmspinbox_NrAcq.showStepExponent = False
        self.pydmlabel_NrAcq = PyDMLabel(
            parent=self,
            init_channel='ca://'+self.prefix+'BO-35D:DI-DCCT:??????-RB')
        hlay_nracq = QHBoxLayout()
        hlay_nracq.addWidget(self.pydmspinbox_NrAcq)
        hlay_nracq.addWidget(self.pydmlabel_NrAcq)

        # TODO: add DCCT PVs control

        l_injcurr_idx = QLabel('Injected current index: ', self,
                               alignment=Qt.AlignRight)
        self.sb_injcurr_idx = QSpinBox(self)
        self.sb_injcurr_idx.setValue(self.injcurr_idx)
        self.sb_injcurr_idx.setMinimum(1)
        self.sb_injcurr_idx.setMaximum(4000)  # TODO: max=len(CurrentHstr PV)
        self.sb_injcurr_idx.setFixedSize(220, 40)

        l_ejecurr_idx = QLabel('Ejected current index: ', self,
                               alignment=Qt.AlignRight)
        self.sb_ejecurr_idx = QSpinBox(self)
        self.sb_ejecurr_idx.setValue(self.ejecurr_idx)
        self.sb_ejecurr_idx.setMinimum(1)
        self.sb_ejecurr_idx.setMaximum(4000)  # TODO: max=len(CurrentHstr PV)
        self.sb_ejecurr_idx.setFixedSize(220, 40)

        flay_settings = QFormLayout()
        flay_settings.addRow(l_dcctacq)
        flay_settings.addRow(l_nracq, hlay_nracq)
        flay_settings.addRow(l_injcurr_idx, self.sb_injcurr_idx)
        flay_settings.addRow(l_ejecurr_idx, self.sb_ejecurr_idx)

        self.bt_apply = QPushButton('Apply settings', self)
        self.bt_apply.clicked.connect(self._emitSettings)
        self.bt_apply.setAutoDefault(False)
        self.bt_apply.setDefault(False)
        hlay_apply = QHBoxLayout()
        hlay_apply.addItem(
            QSpacerItem(40, 20, QSzPlcy.Expanding, QSzPlcy.Fixed))
        hlay_apply.addWidget(self.bt_apply)

        self.setLayout(QVBoxLayout())
        self.layout().addLayout(flay_settings)
        self.layout().addLayout(hlay_apply)

    def _emitSettings(self):
        self.updateSettings.emit([self.sb_injcurr_idx.value(),
                                  self.sb_ejecurr_idx.value()])
        self.close()


class ChooseMagnetsToPlot(SiriusDialog):
    """Auxiliar window to select which magnets will to be shown in plot."""

    choosePlotSignal = Signal(list)

    def __init__(self, parent, manames, current_plots):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Choose Magnets To Plot')
        self.manames = manames
        self.current_plots = current_plots
        self._setupUi()

    def _setupUi(self):
        self.quads = QWidget(self)
        vlay_quad = QVBoxLayout()
        vlay_quad.setAlignment(Qt.AlignTop)
        self.quads.setLayout(vlay_quad)

        self.sexts = QWidget(self)
        vlay_sext = QVBoxLayout()
        vlay_sext.setAlignment(Qt.AlignTop)
        self.sexts.setLayout(vlay_sext)

        self.chs = QWidget(self)
        vlay_ch = QVBoxLayout()
        vlay_ch.setAlignment(Qt.AlignTop)
        self.chs.setLayout(vlay_ch)

        self.cvs = QWidget(self)
        vlay_cv = QVBoxLayout()
        vlay_cv.setAlignment(Qt.AlignTop)
        self.cvs.setLayout(vlay_cv)

        self.all_quad_sel = QCheckBox('All quadrupoles', self.quads)
        self.all_quad_sel.clicked.connect(self._handleSelectGroups)
        vlay_quad.addWidget(self.all_quad_sel)
        self.all_sext_sel = QCheckBox('All sextupoles', self.sexts)
        self.all_sext_sel.clicked.connect(self._handleSelectGroups)
        vlay_sext.addWidget(self.all_sext_sel)
        self.all_ch_sel = QCheckBox('All CHs', self.chs)
        self.all_ch_sel.clicked.connect(self._handleSelectGroups)
        vlay_ch.addWidget(self.all_ch_sel)
        self.all_cv_sel = QCheckBox('All CVs', self.cvs)
        self.all_cv_sel.clicked.connect(self._handleSelectGroups)
        vlay_cv.addWidget(self.all_cv_sel)

        for maname in self.manames:
            if 'Q' in maname:
                cb_maname = QCheckBox(maname, self.quads)
                vlay_quad.addWidget(cb_maname)
            elif 'S' in maname:
                cb_maname = QCheckBox(maname, self.sexts)
                vlay_sext.addWidget(cb_maname)
            elif 'CH' in maname:
                cb_maname = QCheckBox(maname, self.chs)
                vlay_ch.addWidget(cb_maname)
            elif 'CV' in maname:
                cb_maname = QCheckBox(maname, self.cvs)
                vlay_cv.addWidget(cb_maname)
            if maname in self.current_plots:
                cb_maname.setChecked(True)
            cb_maname.setObjectName(maname)

        self.pb_choose = QPushButton('Choose', self)
        self.pb_choose.clicked.connect(self._emitChoosePlot)

        glay = QGridLayout()
        glay.addWidget(self.quads, 0, 0)
        glay.addWidget(self.sexts, 1, 0)
        glay.addWidget(self.chs, 0, 1, 2, 1)
        glay.addWidget(self.cvs, 0, 2, 2, 1)
        glay.addWidget(self.pb_choose, 2, 1)
        self.setLayout(glay)

    def _handleSelectGroups(self):
        sender = self.sender()
        sender_parent = sender.parent()
        for child in sender_parent.children():
            if isinstance(child, QCheckBox):
                child.setChecked(sender.isChecked())

    def _emitChoosePlot(self):
        maname_list = list()
        children = list()
        for w in [self.quads, self.sexts, self.chs, self.cvs]:
            for child in w.children():
                children.append(child)
        for child in children:
            if (isinstance(child, QCheckBox) and child.isChecked() and
                    'BO' in child.objectName()):
                maname_list.append(child.objectName())

        self.choosePlotSignal.emit(maname_list)
        self.close()


class SpinBoxDelegate(QStyledItemDelegate):
    """Auxiliar class to draw a SpinBox in table items on editing."""

    def createEditor(self, parent, option, index):
        """Create editor."""
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(500)
        editor.setDecimals(4)
        locale = QLocale(QLocale.English, country=QLocale.UnitedStates)
        locale.setNumberOptions(locale.RejectGroupSeparator)
        editor.setLocale(locale)
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

    acceptedSignal = Signal()
    regectedSignal = Signal()

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


class MyDoubleSpinBox(QDoubleSpinBox):
    """Subclass QDoubleSpinBox to reimplement whellEvent."""

    def __init__(self, parent):
        """Initialize object."""
        super().__init__(parent)
        locale = QLocale(QLocale.English, country=QLocale.UnitedStates)
        locale.setNumberOptions(locale.RejectGroupSeparator)
        self.setLocale(locale)

    def wheelEvent(self, event):
        """Reimplement wheel event to ignore event when out of focus."""
        if not self.hasFocus():
            event.ignore()
        else:
            super().wheelEvent(event)
