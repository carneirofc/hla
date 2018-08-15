"""Magnet cycle window."""
from math import isclose
import time
import epics

from pydm.PyQt.QtCore import pyqtSignal, QThread
from pydm.PyQt.QtGui import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QDialog, QLabel, QProgressBar, QMessageBox

from siriuspy.envars import vaca_prefix as VACA_PREFIX
from siriushla.as_ps_cycle.cycle_status_list import CycleStatusList
from siriushla.as_ps_cycle.magnets_tree import MagnetTree


class CycleWindow(QMainWindow):
    """Magnet cycle window."""

    def __init__(self, parent=None):
        """Constructor."""
        super().__init__(parent)
        # Data structs
        self._magnets = list()
        self._magnets_ready = list()
        self._magnets_failed = list()
        self._cyclers = list()
        # Setup UI
        self._setup_ui()
        self.setWindowTitle('Magnet Cycling')

    def _setup_ui(self):
        central_widget = QWidget()
        central_widget.layout = QVBoxLayout()
        central_widget.setLayout(central_widget.layout)

        self.prepare_button = QPushButton("Prepare to cycle", self)
        self.magnets_tree = MagnetTree(self)

        central_widget.layout.addWidget(self.magnets_tree)
        central_widget.layout.addWidget(self.prepare_button)

        self.setCentralWidget(central_widget)

        self.prepare_button.pressed.connect(self._prepare_to_cycle)

    def _prepare_to_cycle(self):
        self._magnets = self.magnets_tree.checked_items()
        self._magnets_ready = list()
        self._magnets_failed = list()
        self._cyclers = [MagnetCycler(maname) for maname in self._magnets]

        # Set magnets to proper cycling state
        task1 = SetToCycle(self._cyclers, self)
        task2 = VerifyCycle(self._cyclers, self)
        task2.itemChecked.connect(self._check_cycling_status)
        dlg = ProgressDialog('Setting magnets to cycle...', [task1, task2], self)
        ret = dlg.exec_()
        if ret == dlg.Rejected:
            return
        # Check magnet are in proper cycling state
        # task = VerifyCycle(self._cyclers, self)
        # task.itemChecked.connect(self._check_cycling_status)
        # dlg = ProgressDialog('Checking magnets...', task, self)
        # ret = dlg.exec_()
        # if ret == dlg.Rejected:
        #     return
        # Show failed magnets or ask to cycle
        dlg = CyclingDlg(self._magnets_failed, self)
        ret = dlg.exec_()
        if ret == dlg.Rejected:
            return
        # Wait cyling end
        task = WaitCycle(self._cyclers, self)
        dlg = ProgressDialog('Wait for magnets to cycle...', task, self)
        self._cycle()
        ret = dlg.exec_()
        if ret == dlg.Rejected:
            return

        QMessageBox.information(self, 'Message', 'Cycle finished sucessfully!')
        self.close()

    def _cycle(self):
        def write_pv(pvname, value):
            epics.caput(pvname, value, wait=True)
            time.sleep(0.1)
        write_pv('TAS-Glob:TI-EVG:ContinuousEvt-Sel', 0)
        write_pv('TAS-Glob:TI-EVG:DevEnbl-Sel', 1)
        write_pv('TAS-Glob:TI-EVG:ACDiv-SP', 30)
        write_pv('TAS-Glob:TI-EVG:ACEnbl-Sel', 1)
        write_pv('TAS-Glob:TI-EVG:RFDiv-SP', 4)
        write_pv('TAS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
        write_pv('TAS-Glob:TI-EVR-1:DevEnbl-Sel', 1)
        write_pv('TAS-Glob:TI-EVR-1:OTP08State-Sel', 1)
        write_pv('TAS-Glob:TI-EVR-1:OTP08Width-SP', 7000)
        write_pv('TAS-Glob:TI-EVR-1:OTP08Evt-SP', 1)
        write_pv('TAS-Glob:TI-EVR-1:OTP08Polarity-Sel', 0)
        write_pv('TAS-Glob:TI-EVR-1:OTP08Pulses-SP', 1)
        write_pv('TAS-Glob:TI-EVR-1:OTP08Pulses-SP', 1)
        write_pv('TAS-Glob:TI-EVG:Evt01Mode-Sel', 'External')
        write_pv('TAS-Glob:TI-EVG:Evt01ExtTrig-Cmd', 1)

    def _check_cycling_status(self, cycler, status):
        """Check magnet cycling status."""
        row = self._cyclers.index(cycler)
        if status:
            self._magnets_ready.append(self._magnets[row])
        else:
            self._magnets_failed.append(self._magnets[row])


class MagnetCycler:
    """Handle magnet properties related to cycling."""

    def __init__(self, maname):
        """Constructor."""
        self._maname = maname
        self.pwrstate_sel = epics.get_pv(
            VACA_PREFIX + self._maname + ':PwrState-Sel')
        self.cycletype_sel = \
            epics.get_pv(VACA_PREFIX + self._maname + ':CycleType-Sel')
        self.cyclefreq_sp = \
            epics.get_pv(VACA_PREFIX + self._maname + ':CycleFreq-SP')
        self.cycleampl_sp = \
            epics.get_pv(VACA_PREFIX + self._maname + ':CycleAmpl-SP')
        self.opmode_sel = \
            epics.get_pv(VACA_PREFIX + self._maname + ':OpMode-Sel')
        self.pwrstate_sts = \
            epics.get_pv(VACA_PREFIX + self._maname + ':PwrState-Sts')
        self.cycletype_sts = \
            epics.get_pv(VACA_PREFIX + self._maname + ':CycleType-Sts')
        self.cyclefreq_rb = \
            epics.get_pv(VACA_PREFIX + self._maname + ':CycleFreq-RB')
        self.cycleampl_rb = \
            epics.get_pv(VACA_PREFIX + self._maname + ':CycleAmpl-RB')
        self.opmode_sts = \
            epics.get_pv(VACA_PREFIX + self._maname + ':OpMode-Sts')

        self.pwrstate = 1
        self.cycletype = 0
        self.cyclefreq = 0.3
        self.cycleampl = 2.0
        self.opmode = 2

    @property
    def maname(self):
        """Magnet name."""
        return self._maname

    def set_on(self):
        """Turn magnet PS on."""
        return self.conn_put(self.pwrstate_sel, self.pwrstate)

    def set_params(self):
        """Set cycling params."""
        return (self.conn_put(self.cycletype_sel, self.cycletype) and
                self.conn_put(self.cyclefreq_sp, self.cyclefreq) and
                self.conn_put(self.cycleampl_sp, self.cycleampl))

    def set_mode(self):
        """Set magnet to cycling mode."""
        return self.conn_put(self.opmode_sel, self.opmode)

    def set_cycle(self):
        """Set magnet to cycling mode."""
        self.conn_put(self.opmode_sel, 0)
        self.set_on()
        self.set_params()
        self.set_mode()

    def on_rdy(self):
        """Return wether magnet PS is on."""
        return self.timed_get(self.pwrstate_sts, self.pwrstate)

    def params_rdy(self):
        """Return wether magnet cycling parameters are set."""
        return (self.timed_get(self.cycletype_sts, self.cycletype) and
                self.timed_get(self.cyclefreq_rb, self.cyclefreq) and
                self.timed_get(self.cycleampl_rb, self.cycleampl))

    def mode_rdy(self):
        """Return wether magnet is in cycling mode."""
        return self.timed_get(self.opmode_sts, self.opmode)

    def is_ready(self):
        """Return wether magnet is ready to cycle."""
        return self.on_rdy() and self.params_rdy() and self.mode_rdy()

    def conn_put(self, pv, value):
        """Put if connected."""
        if not pv.connected:
            return False
        if pv.put(value):
            time.sleep(0.1)
            return True
        return False

    def timed_get(self, pv, value, wait=1):
        """Do timed get."""
        if not pv.connected:
            return False
        t = 0
        init = time.time()
        while t < wait:
            if isinstance(value, float):
                if isclose(pv.get(), value, rel_tol=1e-06, abs_tol=0.0):
                    return True

            else:
                if pv.get() == value:
                    return True
            t = time.time() - init
            time.sleep(0.1)
        return False


class ProgressDialog(QDialog):
    """Progress dialog."""

    canceled = pyqtSignal()

    def __init__(self, label, task, parent=None):
        """Constructor."""
        super().__init__(parent)
        self._label = label
        self._task = task
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        self.cancel = QPushButton('Cancel', self)

        self.layout.addWidget(QLabel(self._label))
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.cancel)

        self.setLayout(self.layout)

        # Set progress bar limit
        self.progress_bar.setMinimum(0)
        # Signals
        self.cancel.pressed.connect(self.canceled.emit)
        self.canceled.connect(lambda: self._exit_dlg(0))
        self.progress_bar.valueChanged.connect(self._is_finished)

        if hasattr(self._task, '__iter__'):
            self._task[0].itemDone.connect(self.inc_value)
            self.progress_bar.setMaximum(self._task[0].size())
            for i in range(1, len(self._task)):
                self._task[i].itemDone.connect(self.inc_value)
                self._task[i - 1].finished.connect(self._task[i].start)
                self.progress_bar.setMaximum(self.progress_bar.maximum() +
                                             self._task[i].size())
            self._task[-1].finished.connect(lambda: self._exit_dlg(1))
        else:
            self._task.itemDone.connect(self.inc_value)
            self._task.finished.connect(lambda: self._exit_dlg(1))
            self.progress_bar.setMaximum(self._task.size())

    def _exit_dlg(self, result):
        if hasattr(self._task, '__iter__'):
            # for task in self._task:
            self._task[-1].exit_task()
            self._wait_task(self._task[-1])
            self._task[-1].deleteLater()
        else:
            self._task.exit_task()
            self._wait_task(self._task)
            self._task.deleteLater()
        if result == 1:
            self.accept()
        elif result == 0:
            self.reject()

    def _wait_task(self, task):
        init = time.time()
        try:
            while task.isRunning():
                time.sleep(0.1)
                if time.time() - init > 10:
                    self._exit_dlg(0)
                    raise Exception('Thread will not leave')
        except RuntimeError:
            pass

    def _is_finished(self):
        if self.progress_bar.maximum() == self.progress_bar.value():
            self._exit_dlg(0)

    def set_value(self, value):
        """Set progress bar value."""
        self.progress_bar.setValue(value)

    def inc_value(self):
        """Increase value."""
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def exec_(self):
        """Override."""
        if hasattr(self._task, '__iter__'):
            self._task[0].start()
        else:
            self._task.start()
        return super().exec_()


class CyclingDlg(QDialog):
    """Magnet cycle dialog."""

    def __init__(self, magnets, parent=None):
        """Constructor."""
        super().__init__(parent)
        self._magnets = magnets

        self._cyclers = dict()
        for magnet in magnets:
            self._cyclers[magnet] = MagnetCycler(magnet)

        # Setup user interface
        self._setup_ui()
        self._connect_buttons()

    def _setup_ui(self):
        layout = QVBoxLayout()

        btn_group = QHBoxLayout()
        self.cycle_btn = QPushButton('Cycle', self)
        self.cancel_btn = QPushButton('Cancel', self)
        btn_group.addWidget(self.cycle_btn)
        btn_group.addWidget(self.cancel_btn)
        if not self._magnets:
            self.label = QLabel('All magnets ready to cycle', self)
            self.status_list = None
            layout.addWidget(self.label)
            layout.addLayout(btn_group)
        else:
            self.label = QLabel(
                'Failed to set {} magnets'.format(len(self._magnets)), self)
            self.cycle_btn.setEnabled(False)
            self.status_list = CycleStatusList(self._magnets)

            layout.addWidget(self.status_list)
            layout.addWidget(self.label)
            layout.addLayout(btn_group)

        self.setLayout(layout)

    def _connect_buttons(self):
        self.cycle_btn.pressed.connect(self.accept)
        self.cancel_btn.pressed.connect(self.reject)


class SetToCycle(QThread):
    """Set magnet to cycle."""

    itemDone = pyqtSignal()

    def __init__(self, cyclers, parent=None):
        """Constructor."""
        super().__init__(parent)
        self._cyclers = cyclers
        self._quit_task = False

    def size(self):
        """Return task size."""
        return len(self._cyclers)

    def exit_task(self):
        """Set flag to quit thread."""
        self._quit_task = True

    def run(self):
        """Set magnets to cycling."""
        if self._quit_task:
            self.finished.emit()
        else:
            for cycler in self._cyclers:
                cycler.set_cycle()
                self.itemDone.emit()
                if self._quit_task:
                    break
            self.finished.emit()


class VerifyCycle(QThread):
    """Verify cycle."""

    currentItem = pyqtSignal(MagnetCycler)
    itemDone = pyqtSignal()
    itemChecked = pyqtSignal(MagnetCycler, bool)

    def __init__(self, cyclers, parent=None):
        """Constructor."""
        super().__init__(parent)
        self._cyclers = cyclers
        self.quit_task = False

    def size(self):
        """Return task size."""
        return len(self._cyclers)

    def exit_task(self):
        """Set flag to quit thread."""
        self.quit_task = True

    def run(self):
        """Set magnets to cycling."""
        if self.quit_task:
            self.finished.emit()
        else:
            time.sleep(2)
            for cycler in self._cyclers:
                self.currentItem.emit(cycler)
                status = cycler.is_ready()
                if self.quit_task:
                    break
                self.itemDone.emit()
                self.itemChecked.emit(cycler, status)
            self.finished.emit()


class WaitCycle(QThread):
    """Cycle."""

    itemDone = pyqtSignal()

    def __init__(self, cyclers, parent=None):
        """Build PVs."""
        super().__init__(parent)
        self._cyclers = cyclers
        self.quit_task = False

        field = ':CycleEnbl-Mon'
        self.pvs = \
            {cycler.maname: epics.get_pv(cycler.maname + field)
             for cycler in cyclers}
        self.pvs_state = {maname + field: 0 for maname in self.pvs}

        self.ps_count = len(self.pvs)
        self.ps_cycled = 0

        for pv in self.pvs.values():
            pv.add_callback(self.check_cycle_end)

    def size(self):
        """Return task size."""
        return len(self._cyclers)

    def exit_task(self):
        """Set flag to quit thread."""
        self.quit_task = True

    def run(self):
        """Start thread."""
        while self.ps_cycled < self.ps_count:
            time.sleep(0.1)
            if self.quit_task:
                break
        self.finished.emit()

    def check_cycle_end(self, pvname, value, cb_info, **kwargs):
        """Check wether cycle finished."""
        state = self.pvs_state[pvname]
        if state == 0:
            if value == 0:
                pass
            elif value == 1:
                self.pvs_state[pvname] = 1
        elif state == 1:
            if value == 0:
                cb_info[1].remove_callback(cb_info[0])
                self.itemDone.emit()
                self.ps_cycled += 1
            elif value == 1:
                pass


if __name__ == '__main__':
    import sys
    from siriushla.sirius_application import SiriusApplication

    app = SiriusApplication()

    w = CycleWindow()
    # w.setStyleSheet("font-size: 16pt;")
    w.show()

    sys.exit(app.exec_())