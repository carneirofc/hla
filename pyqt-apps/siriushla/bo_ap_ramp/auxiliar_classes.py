"""Booster Ramp Control HLA: Auxiliar Classes Module."""

from qtpy.QtCore import Qt, Signal, Slot, QLocale
from qtpy.QtWidgets import QLabel, QWidget, QAbstractItemView, QMessageBox, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QCheckBox, \
    QTableWidget, QTableWidgetItem, QRadioButton, QFormLayout, QDoubleSpinBox,\
    QComboBox, QSpinBox, QStyledItemDelegate, QSpacerItem, QTabWidget, \
    QSizePolicy as QSzPlcy, QHeaderView

from siriuspy.clientconfigdb import ConfigDBClient as _ConfigDBClient, \
    ConfigDBDocument as _ConfigDBDocument, \
    ConfigDBException as _ConfigDBException
from siriuspy.ramp import ramp

from siriushla.widgets.windows import SiriusDialog
from siriushla.as_ap_configdb import LoadConfigDialog as _LoadConfigDialog, \
                                     SaveConfigDialog as _SaveConfigDialog


class LoadRampConfig(_LoadConfigDialog):
    """Auxiliar window to get a ramp config name to load."""

    loadSignal = Signal()
    saveSignal = Signal()

    def __init__(self, ramp_config, parent=None):
        """Initialize object."""
        self.ramp_config = ramp_config
        super().__init__('bo_ramp', parent)
        self.setWindowTitle('Load ramp configuration from server')

    @Slot()
    def _load_configuration(self):
        name = self.config_name
        if self.ramp_config is not None:
            if not self.ramp_config.synchronized:
                ans = QMessageBox.question(
                    self, 'Save changes?',
                    'There are unsaved changes in {}. \n'
                    'Do you want to save?'.format(name),
                    QMessageBox.Yes, QMessageBox.Cancel)
                if ans == QMessageBox.Yes:
                    self.saveSignal.emit()

            if name != self.ramp_config.name:
                self.configname.emit(name)
            else:
                self.loadSignal.emit()
        else:
            self.configname.emit(name)
        self.accept()


class NewRampConfigGetName(_SaveConfigDialog):
    """Auxiliar window to get a configuration name to create a new one."""

    saveSignal = Signal()

    def __init__(self, config, config_type, parent=None,
                 new_from_template=True):
        """Initialize object."""
        super().__init__(config_type, parent)
        self.config = config
        self.config_type = config_type
        self._new_from_template = new_from_template
        if new_from_template:
            self.setWindowTitle('New config from template')
            self.ok_button.setText('Create')
        else:
            self.setWindowTitle('Save current config as...')
            self.ok_button.setText('Save as...')

    @Slot()
    def _load_configuration(self):
        name = self.config_name
        if (self._new_from_template and (self.config is not None)):
            if not self.config.synchronized:
                ans = QMessageBox.question(
                    self, 'Save changes?',
                    'There are unsaved changes in {}. \n'
                    'Do you want to save?'.format(name),
                    QMessageBox.Yes, QMessageBox.Cancel)
                if ans == QMessageBox.Yes:
                    self.saveSignal.emit()
            else:
                self.configname.emit(name)
                self.accept()
        else:
            self.configname.emit(name)
            self.accept()


class InsertNormalizedConfig(SiriusDialog):
    """Auxiliar window to insert a new normalized config."""

    insertConfig = Signal(list)

    def __init__(self, parent, ramp_config):
        """Initialize object."""
        super().__init__(parent)
        self.ramp_config = ramp_config
        self.norm_config = ramp.BoosterNormalized()
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
        vlay.addItem(QSpacerItem(40, 20, QSzPlcy.Ignored, QSzPlcy.Preferred))
        vlay.addWidget(
            QLabel('<h4>Insert a Normalized Configuration</h4>', self),
            alignment=Qt.AlignCenter)
        vlay.addItem(QSpacerItem(40, 20, QSzPlcy.Ignored, QSzPlcy.Preferred))
        vlay.addWidget(self.rb_interp)
        vlay.addWidget(self.rb_confsrv)
        vlay.addWidget(self.rb_create)
        vlay.addItem(QSpacerItem(40, 20, QSzPlcy.Ignored, QSzPlcy.Preferred))
        vlay.addWidget(self.config_data)

        self.setLayout(vlay)
        self.setStyleSheet("""
            #interp_settings{
                min-width:20em;max-width:20em;
                min-height:6em;max-height:6em;}
            #confsrv_settings{
                min-width:20em;max-width:20em;
                min-height:6em;max-height:6em;}
            #create_settings{
                min-width:20em;max-width:20em;
                min-height:6em;max-height:6em;}""")

    def _setupConfigDataWidget(self):
        vlay = QVBoxLayout()
        self.interp_settings = QWidget()
        self.interp_settings.setObjectName('interp_settings')
        self.confsrv_settings = QWidget()
        self.confsrv_settings.setObjectName('confsrv_settings')
        self.create_settings = QWidget()
        self.create_settings.setObjectName('create_settings')
        self.confsrv_settings.setVisible(False)
        self.create_settings.setVisible(False)
        vlay.addWidget(self.interp_settings)
        vlay.addWidget(self.confsrv_settings)
        vlay.addWidget(self.create_settings)
        self.config_data.setLayout(vlay)

        # to insert interpolating existing norm configs
        flay_interp = QFormLayout()
        self.le_interp_name = QLineEdit(self)
        self.le_interp_name.setText(_ConfigDBDocument.generate_config_name())
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
        self.le_confsrv_name = _ConfigLineEdit(self)
        self.le_confsrv_name.textChanged.connect(
            self._handleInsertExistingConfig)
        self.sb_confsrv_time = QDoubleSpinBox(self)
        self.sb_confsrv_time.setMaximum(490)
        self.sb_confsrv_time.setDecimals(6)
        self.bt_confsrv = QPushButton('Insert', self)
        self.bt_confsrv.setAutoDefault(False)
        self.bt_confsrv.setDefault(False)
        self.bt_confsrv.clicked.connect(self._emitInsertConfigData)
        flay_confsrv.addRow(QLabel('Name: ', self), self.le_confsrv_name)
        flay_confsrv.addRow(QLabel('Time: ', self), self.sb_confsrv_time)
        flay_confsrv.addRow(self.bt_confsrv)

        # to insert a new norm config equal to template
        flay_create = QFormLayout()
        self.le_create_name = QLineEdit(self)
        self.le_create_name.setText(self.norm_config.generate_config_name())
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

    @Slot(str)
    def _handleInsertExistingConfig(self, configname):
        try:
            nor = ramp.BoosterNormalized(configname)
            nor.load()
            energy = nor[ramp.BoosterRamp.MANAME_DIPOLE]
            time = self.ramp_config.ps_waveform_interp_time(energy)
            self.sb_confsrv_time.setValue(time)
        except _ConfigDBException as err:
            QMessageBox.critical(self, 'Error', str(err), QMessageBox.Ok)

    def _emitInsertConfigData(self):
        sender = self.sender()
        data = list()
        if sender is self.bt_interp:
            time = self.sb_interp_time.value()
            name = self.le_interp_name.text()
            nconf = None
        elif sender is self.bt_confsrv:
            time = self.sb_confsrv_time.value()
            name = self.le_confsrv_name.text()
            nconf = None
            try:
                nor = ramp.BoosterNormalized(name)
                nor.load()
                nconf = nor.value
            except _ConfigDBException as err:
                QMessageBox.critical(self, 'Error', str(err), QMessageBox.Ok)

        elif sender is self.bt_create:
            time = self.sb_create_time.value()
            name = self.le_create_name.text()
            nconf = self.norm_config.get_value_template()
        data = [time, name, nconf]
        self.insertConfig.emit(data)
        self.close()


class DeleteNormalizedConfig(SiriusDialog):
    """Auxiliar window to delete a normalized config."""

    deleteConfig = Signal(str)

    def __init__(self, parent, table_map, selected_item):
        """Initialize object."""
        super().__init__(parent)
        self.norm_config = ramp.BoosterNormalized()
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
        self.sb_confignumber.setStyleSheet("""max-width:5em;""")
        self.sb_confignumber.valueChanged.connect(self._searchConfigByIndex)
        self.bt_delete = QPushButton('Delete', self)
        self.bt_delete.setAutoDefault(False)
        self.bt_delete.setDefault(False)
        self.bt_delete.clicked.connect(self._emitDeleteConfigData)
        self.l_configname = QLabel('', self)
        self.l_configname.setSizePolicy(QSzPlcy.MinimumExpanding,
                                        QSzPlcy.Expanding)
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


class OpticsAdjustSettings(SiriusDialog):
    """Auxiliar window to optics adjust settings."""

    updateSettings = Signal(str, str)

    def __init__(self, tuneconfig_currname, chromconfig_currname, parent=None):
        """Initialize object."""
        super().__init__(parent)
        self.setWindowTitle('Optics Adjust Settings')
        self.tuneconfig_currname = tuneconfig_currname
        self.chromconfig_currname = chromconfig_currname
        self.conn_tuneparams = _ConfigDBClient(
            config_type='bo_tunecorr_params')
        self.conn_chromparams = _ConfigDBClient(
            config_type='bo_chromcorr_params')
        self._setupUi()

        try:
            infos = self.conn_tuneparams.find_configs()
            for info in infos:
                self.cb_tuneconfig.addItem(info['name'])

            infos = self.conn_chromparams.find_configs()
            for info in infos:
                self.cb_chromconfig.addItem(info['name'])
        except _ConfigDBException as err:
            QMessageBox.critical(self, 'Error', str(err), QMessageBox.Ok)
        finally:
            self.cb_tuneconfig.setCurrentText(self.tuneconfig_currname)
            self._showTuneConfigData()
            self.cb_chromconfig.setCurrentText(self.chromconfig_currname)
            self._showChromConfigData()

    def _setupUi(self):
        self.tune_settings = QWidget(self)
        self.tune_settings.setLayout(self._setupTuneSettings())
        self.chrom_settings = QWidget(self)
        self.chrom_settings.setLayout(self._setupChromSettings())
        self.bt_apply = QPushButton('Apply Settings', self)
        self.bt_apply.setStyleSheet("""min-width:8em; max-width:8em;""")
        self.bt_apply.clicked.connect(self._emitSettings)
        self.bt_apply.setAutoDefault(False)
        self.bt_apply.setDefault(False)
        hlay_apply = QHBoxLayout()
        hlay_apply.addItem(
            QSpacerItem(20, 60, QSzPlcy.Expanding, QSzPlcy.Ignored))
        hlay_apply.addWidget(self.bt_apply)

        tabs = QTabWidget(self)
        tabs.addTab(self.tune_settings, 'Tune')
        tabs.addTab(self.chrom_settings, 'Chromaticity')

        lay = QVBoxLayout()
        lay.addWidget(tabs)
        lay.addLayout(hlay_apply)

        self.setLayout(lay)

    def _setupTuneSettings(self):
        l_tuneconfig = QLabel('<h3>Tune Variation Config</h3>', self)
        l_tuneconfig.setAlignment(Qt.AlignCenter)
        self.cb_tuneconfig = QComboBox(self)
        self.cb_tuneconfig.setEditable(True)
        self.cb_tuneconfig.currentTextChanged.connect(self._showTuneConfigData)

        label_tunemat = QLabel('<h4>Matrix</h4>', self)
        label_tunemat.setAlignment(Qt.AlignCenter)
        self.table_tunemat = QTableWidget(self)
        self.table_tunemat.setObjectName('tunemat')
        self.table_tunemat.setStyleSheet("""
            #tunemat{
                background-color: #efebe7;
                min-width: 22.14em;
                min-height: 6em; max-height: 6em;}""")
        self.table_tunemat.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_tunemat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_tunemat.setRowCount(2)
        self.table_tunemat.setColumnCount(2)
        self.table_tunemat.setVerticalHeaderLabels(['  X', '  Y'])
        self.table_tunemat.setHorizontalHeaderLabels(['QF', 'QD'])
        self.table_tunemat.horizontalHeader().setStyleSheet("""
            min-height:1.55em; max-height:1.55em;""")
        self.table_tunemat.verticalHeader().setStyleSheet("""
            min-width:1.55em; max-width:1.55em;""")
        self.table_tunemat.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_tunemat.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_tunemat.setSizePolicy(QSzPlcy.MinimumExpanding,
                                         QSzPlcy.Preferred)

        label_nomKL = QLabel('<h4>Nominal KL</h4>')
        label_nomKL.setAlignment(Qt.AlignCenter)
        self.table_nomKL = QTableWidget(self)
        self.table_nomKL.setObjectName('nomKL')
        self.table_nomKL.setStyleSheet("""
            #nomKL{
                background-color: #efebe7;
                min-width: 22.14em;
                min-height: 4em; max-height: 4em;}""")
        self.table_nomKL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_nomKL.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_nomKL.setRowCount(1)
        self.table_nomKL.setColumnCount(2)
        self.table_nomKL.setVerticalHeaderLabels(['KL'])
        self.table_nomKL.setHorizontalHeaderLabels(['QF', 'QD'])
        self.table_nomKL.horizontalHeader().setStyleSheet("""
            min-height:1.55em; max-height:1.55em;""")
        self.table_nomKL.verticalHeader().setStyleSheet("""
            min-width:1.55em; max-width:1.55em;""")
        self.table_nomKL.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_nomKL.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_nomKL.setSizePolicy(QSzPlcy.MinimumExpanding,
                                       QSzPlcy.Preferred)

        lay = QVBoxLayout()
        lay.addWidget(l_tuneconfig)
        lay.addWidget(self.cb_tuneconfig)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Ignored, QSzPlcy.Expanding))
        lay.addWidget(label_tunemat)
        lay.addWidget(self.table_tunemat)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Ignored, QSzPlcy.Expanding))
        lay.addWidget(label_nomKL)
        lay.addWidget(self.table_nomKL)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Ignored, QSzPlcy.Expanding))

        return lay

    def _setupChromSettings(self):
        l_chromconfig = QLabel('<h3>Chromaticity Variation Config</h3>', self)
        l_chromconfig.setAlignment(Qt.AlignCenter)
        self.cb_chromconfig = QComboBox(self)
        self.cb_chromconfig.setEditable(True)
        self.cb_chromconfig.currentTextChanged.connect(
            self._showChromConfigData)

        l_chrommat = QLabel('<h4>Matrix</h4>', self)
        l_chrommat.setAlignment(Qt.AlignCenter)
        self.table_chrommat = QTableWidget(self)
        self.table_chrommat.setObjectName('chrommat')
        self.table_chrommat.setStyleSheet("""
            #chrommat{
                background-color: #efebe7;
                min-width: 22.14em;
                min-height: 6em; max-height: 6em;}""")
        self.table_chrommat.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_chrommat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_chrommat.setRowCount(2)
        self.table_chrommat.setColumnCount(2)
        self.table_chrommat.setVerticalHeaderLabels(['  X', '  Y'])
        self.table_chrommat.setHorizontalHeaderLabels(['SF', 'SD'])
        self.table_chrommat.horizontalHeader().setStyleSheet("""
            min-height:1.55em; max-height:1.55em;""")
        self.table_chrommat.verticalHeader().setStyleSheet("""
            min-width:1.55em; max-width:1.55em;""")
        self.table_chrommat.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_chrommat.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_chrommat.setSizePolicy(QSzPlcy.MinimumExpanding,
                                          QSzPlcy.Preferred)

        l_nomSL = QLabel('<h4>Nominal SL</h4>')
        l_nomSL.setAlignment(Qt.AlignCenter)
        self.table_nomSL = QTableWidget(self)
        self.table_nomSL.setObjectName('nomSL')
        self.table_nomSL.setStyleSheet("""
            #nomSL{
                background-color: #efebe7;
                min-width: 22.14em;
                min-height: 4em; max-height: 4em;}""")
        self.table_nomSL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_nomSL.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_nomSL.setRowCount(1)
        self.table_nomSL.setColumnCount(2)
        self.table_nomSL.setVerticalHeaderLabels(['SL'])
        self.table_nomSL.setHorizontalHeaderLabels(['SF', 'SD'])
        self.table_nomSL.horizontalHeader().setStyleSheet("""
            min-height:1.55em; max-height:1.55em;""")
        self.table_nomSL.verticalHeader().setStyleSheet("""
            min-width:1.55em; max-width:1.55em;""")
        self.table_nomSL.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_nomSL.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.table_nomSL.setSizePolicy(QSzPlcy.MinimumExpanding,
                                       QSzPlcy.Preferred)

        l_nomchrom = QLabel('<h4>Nominal Chrom</h4>')
        l_nomchrom.setAlignment(Qt.AlignCenter)
        self.label_nomchrom = QLabel()
        self.label_nomchrom.setAlignment(Qt.AlignCenter)

        lay = QVBoxLayout()
        lay.addWidget(l_chromconfig)
        lay.addWidget(self.cb_chromconfig)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Expanding, QSzPlcy.Expanding))
        lay.addWidget(l_chrommat)
        lay.addWidget(self.table_chrommat)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Expanding, QSzPlcy.Expanding))
        lay.addWidget(l_nomSL)
        lay.addWidget(self.table_nomSL)
        lay.addItem(QSpacerItem(20, 10, QSzPlcy.Expanding, QSzPlcy.Expanding))
        lay.addWidget(l_nomchrom)
        lay.addWidget(self.label_nomchrom)

        return lay

    @Slot(str)
    def _showTuneConfigData(self):
        try:
            config = self.conn_tuneparams.get_config_value(
                name=self.tuneconfig_currname)
            mat = config['matrix']
            nomKL = config['nominal KLs']
        except _ConfigDBException as err:
            QMessageBox.critical(self, 'Error', str(err), QMessageBox.Ok)
        else:
            self.table_tunemat.setItem(0, 0, QTableWidgetItem(str(mat[0][0])))
            self.table_tunemat.setItem(0, 1, QTableWidgetItem(str(mat[0][1])))
            self.table_tunemat.setItem(1, 0, QTableWidgetItem(str(mat[1][0])))
            self.table_tunemat.setItem(1, 1, QTableWidgetItem(str(mat[1][1])))
            self.table_tunemat.item(0, 0).setFlags(Qt.ItemIsEnabled)
            self.table_tunemat.item(0, 1).setFlags(Qt.ItemIsEnabled)
            self.table_tunemat.item(1, 0).setFlags(Qt.ItemIsEnabled)
            self.table_tunemat.item(1, 1).setFlags(Qt.ItemIsEnabled)
            self.table_nomKL.setItem(0, 0, QTableWidgetItem(str(nomKL[0])))
            self.table_nomKL.setItem(0, 1, QTableWidgetItem(str(nomKL[1])))
            self.table_nomKL.item(0, 0).setFlags(Qt.ItemIsEnabled)
            self.table_nomKL.item(0, 1).setFlags(Qt.ItemIsEnabled)

    @Slot(str)
    def _showChromConfigData(self):
        try:
            config = self.conn_chromparams.get_config_value(
                name=self.chromconfig_currname)
            mat = config['matrix']
            nomSL = config['nominal SLs']
            nomChrom = config['nominal chrom']
        except _ConfigDBException as err:
            QMessageBox.critical(self, 'Error', str(err), QMessageBox.Ok)
        else:
            self.table_chrommat.setItem(0, 0, QTableWidgetItem(str(mat[0][0])))
            self.table_chrommat.setItem(0, 1, QTableWidgetItem(str(mat[0][1])))
            self.table_chrommat.setItem(1, 0, QTableWidgetItem(str(mat[1][0])))
            self.table_chrommat.setItem(1, 1, QTableWidgetItem(str(mat[1][1])))
            self.table_chrommat.item(0, 0).setFlags(Qt.ItemIsEnabled)
            self.table_chrommat.item(0, 1).setFlags(Qt.ItemIsEnabled)
            self.table_chrommat.item(1, 0).setFlags(Qt.ItemIsEnabled)
            self.table_chrommat.item(1, 1).setFlags(Qt.ItemIsEnabled)
            self.table_nomSL.setItem(0, 0, QTableWidgetItem(str(nomSL[0])))
            self.table_nomSL.setItem(0, 1, QTableWidgetItem(str(nomSL[1])))
            self.table_nomSL.item(0, 0).setFlags(Qt.ItemIsEnabled)
            self.table_nomSL.item(0, 1).setFlags(Qt.ItemIsEnabled)
            self.label_nomchrom.setText(str(nomChrom))

    def _emitSettings(self):
        tuneconfig_name = self.cb_tuneconfig.currentText()
        chromconfig_name = self.cb_chromconfig.currentText()
        self.updateSettings.emit(tuneconfig_name, chromconfig_name)
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
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        """Reimplement wheel event to ignore event when out of focus."""
        if not self.hasFocus():
            event.ignore()
        else:
            super().wheelEvent(event)


class _ConfigLineEdit(QLineEdit):

    def mouseReleaseEvent(self, ev):
        popup = _LoadConfigDialog('bo_normalized')
        popup.configname.connect(self.setText)
        popup.exec_()
