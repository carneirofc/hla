"""Read configuration window."""
import logging
import re
import time

from qtpy.QtCore import Slot
from qtpy.QtGui import QKeySequence, QKeyEvent
from qtpy.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, \
    QHBoxLayout, QVBoxLayout, QTableView, QInputDialog, QMessageBox, \
    QAbstractItemView, QApplication

from siriushla.widgets.windows import SiriusMainWindow

from siriushla.misc.epics.wrapper import PyEpicsWrapper
from siriushla.misc.epics.task import EpicsGetter
from siriushla.widgets.dialog import ReportDialog, ProgressDialog
from siriushla.model import \
    ConfigTypeModel, PVConfigurationTableModel
from siriushla.as_ap_pvsconfmgr.delegate import PVConfigurationDelegate
from siriushla.as_ap_servconf import SaveConfiguration
from siriuspy.envars import vaca_prefix as _VACA_PREFIX


class CustomTable(QTableView):

    def keyPressEvent(self, event):
        if event.type() == QKeyEvent.KeyPress:
            if event.matches(QKeySequence.Copy):
                indexes = self.selectionModel().selectedIndexes()
                if len(indexes) == 1:
                    index = indexes[0]
                    if index.column() == 2:
                        value = self.model().data(index)
                        QApplication.instance().clipboard().setText(str(value))
                else:
                    QMessageBox.information(
                        self, 'Copy', 'No support for multi-cell copying')
            elif event.matches(QKeySequence.Paste):
                value = QApplication.instance().clipboard().text()
                indexes = self.selectionModel().selectedIndexes()
                for index in indexes:
                    self.pasteDelay(index, value)

    def pasteDelay(self, index, value):
        if index.column() != 2:
            return
        try:
            value = float(value)
        except ValueError:
            return
        
        self.model().setData(index, value)


class ReadConfigurationWindow(SiriusMainWindow):
    """Read configuration window."""

    def __init__(self, db, wrapper=PyEpicsWrapper, parent=None):
        """Constructor."""
        super().__init__(parent)
        self._db = db
        self._wrapper = wrapper

        self._current_config = None
        self._valid_config = False

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self._setup_ui()
        self._central_widget.setStyleSheet("""
            #CentralWidget {
                min-width: 40em;
                min-height: 40em;
            }
        """)
        self.setWindowTitle('Create new configuration')

    def _setup_ui(self):
        # Set central widget
        self._central_widget = QWidget()
        self._central_widget.setObjectName('CentralWidget')
        self._central_widget.layout = QVBoxLayout()
        self._central_widget.setLayout(self._central_widget.layout)
        self.setCentralWidget(self._central_widget)

        # Add combo box with types
        self._type_cb = QComboBox(self)
        self._type_cb.setObjectName('type_cb')
        self._type_cb.setModel(ConfigTypeModel(self._db, self._type_cb))

        # Add LineEdit for configuration name
        # self._name_le = QLineEdit(self)
        # self._name_le.setObjectName('name_le')

        # Add configuration table
        self._table = CustomTable(self)
        self._table.setObjectName('config_tbl')
        self._table.setModel(PVConfigurationTableModel())
        self._table.setItemDelegate(PVConfigurationDelegate())

        # Add Read Button
        self._read_btn = QPushButton('Read', self)
        self._read_btn.setObjectName('read_btn')
        self._read_btn.setEnabled(False)

        # Add Save Button
        self._save_btn = QPushButton('Save', self)
        self._save_btn.setObjectName('save_btn')
        self._save_btn.setEnabled(False)

        # Add widgets
        self._central_widget.layout.addWidget(self._type_cb)
        # self._central_widget.layout.addWidget(self._name_le)
        self._central_widget.layout.addWidget(self._read_btn)
        self._central_widget.layout.addWidget(self._table)
        self._central_widget.layout.addWidget(self._save_btn)

        # Add signals
        self._type_cb.currentTextChanged.connect(self._fill_table)
        self._read_btn.clicked.connect(self._read)
        self._save_btn.clicked.connect(self._save)

    @Slot(str)
    def _fill_table(self, config_type):
        self._table.model().config_type = config_type
        self._table.resizeColumnsToContents()
        self._is_configuration_valid()

    @Slot()
    def _read(self):
        failed_items = []
        tbl_data = self._table.model().model_data
        # Get PVs
        vp = _VACA_PREFIX
        pvs = {tbl_data[i][0]: i for i in range(len(tbl_data))}
        if len(pvs) != len(tbl_data):
            QMessageBox.warning(
                self, 'Error', 'Configuration has duplicated values')
            return
        # Create thread to read PVs
        task = EpicsGetter(list(pvs), self._wrapper, parent=self)
        task.itemRead.connect(
            lambda pv, value: self._fill_value(pvs[pv.replace(vp, '')], value))
        task.itemNotRead.connect(failed_items.append)
        # Show progress dialog
        time.sleep(1)
        dlg = ProgressDialog('Reading PVs...', task, self)
        ret = dlg.exec_()
        if ret == dlg.Rejected:
            return
        # Show failed items
        for item in failed_items:
            self.logger.warn('Failed to get {}'.format(item))
        self._report = ReportDialog(failed_items, self)
        self._report.show()
        self._table.resizeColumnsToContents()
        # if not failed_items:
        self._save_btn.setEnabled(True)

    @Slot()
    def _fill_value(self, row, value):
        self.logger.info('Setting value {} in row {}'.format(value, row))
        index = self._table.model().createIndex(row, 1)
        self._table.model().setData(index, value)

    def _save(self):
        config_type = self._type_cb.currentText()

        success = False
        error = ''
        label = 'Please select a name'
        # Ask for a name until it is either canceled or succesfully inserted
        while not success:
            # config_name, status = QInputDialog.getText(
            #     self, 'Configuration Name', error + label)

            config_name, status = SaveConfiguration(config_type, self).exec()
            print(config_name, status)

            # Check status and configuration name
            if not re.match('^((\w|[()])+([-_/](\w+|[()])])?)+$', config_name):
                self.logger.warning('Name not allowed')
                error = 'Name not allowed<br>'
                continue
            else:
                success = True

        # Get config_type, config_name, data and insert new configuration
        data = self._table.model().model_data
        try:
            ret = self._db.insert_config(
                config_type, config_name, {'pvs': data})
        except TypeError as e:
            QMessageBox.warning(self, 'Save', '{}'.format(e))
            success = True
        else:
            if ret['code'] == 200:  # Worked
                success = True
                self._save_btn.setEnabled(False)
                QMessageBox.information(self, 'Save', 'Saved successfully')
            else:  # Smth went wrong
                code, message = ret['code'], ret['message']
                self.logger.warning('Error {}: {}'.format(code, message))
                if code == 409:
                    error = 'Name already taken'
                else:
                    error = message
                    error += '<br/><br/>'

    def _is_configuration_valid(self):
        if self._table.model().model_data:
            self._config_valid = True
        else:
            self._config_valid = False
        self._read_btn.setEnabled(self._config_valid)


if __name__ == '__main__':
    import sys
    from siriushla.sirius_application import SiriusApplication
    from siriuspy.servconf.conf_service import ConfigService

    app = SiriusApplication()
    db = ConfigService('http://10.0.7.55:8085')
    w = ReadConfigurationWindow(db)
    w.show()

    sys.exit(app.exec_())