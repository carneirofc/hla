"""PVName selection tree view."""
import re
import uuid
from qtpy.QtCore import Qt, QSize, Signal, QThread
from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem, QProgressDialog, \
    QAction, QMenu

from siriuspy.namesys import SiriusPVName


class QTreeItem(QTreeWidgetItem):
    """Tree Item."""

    def __init__(self, string_list, parent=None):
        """Init."""
        super().__init__(parent, string_list)
        self._shown = set()
        self._status = {
            Qt.Checked: set(), Qt.Unchecked: set(), Qt.PartiallyChecked: set()}
        self._myhash = uuid.uuid4()

    @property
    def myhash(self):
        return self._myhash

    def isLeaf(self):
        """Return if is Leaf."""
        if self.childCount() > 0:
            return False
        return True

    def setHidden(self, status):
        """Overhide setHidden method."""
        super().setHidden(status)
        if isinstance(self.parent(), QTreeItem):
            self.parent().childHidden(self, status)

    def childHidden(self, child, status):
        """Set child hidden."""
        getattr(self._shown, 'discard' if status else 'add')(child.myhash)
        status = not self._shown
        super().setHidden(status)
        if isinstance(self.parent(), QTreeItem):
            self.parent().childHidden(self, status)

    def setData(self, column, role, value):
        """Set data."""
        if column == 0 and role == Qt.CheckStateRole:
            if self.checkState(0) == Qt.PartiallyChecked:
                value = Qt.Unchecked
            # Trigger parent check
            if isinstance(self.parent(), QTreeItem):
                self.parent().childChecked(self, column, value)
            # Trigger children check
            if value in (Qt.Checked, Qt.Unchecked):
                if self.childCount() == 0:
                    if self.checkState(column) != value:
                        self.treeWidget().itemChecked.emit(self, column, value)
                    super().setData(column, role, value)
                else:
                    for c in range(self.childCount()):
                        if not self.child(c).isHidden():
                            self.child(c).setData(
                                column, Qt.CheckStateRole, value)
        else:
            super().setData(column, role, value)

    def _check_children(self):
        """Child was checked."""
        check = self._status
        if check[Qt.PartiallyChecked]:
            return Qt.PartiallyChecked
        elif check[Qt.Checked] and check[Qt.Unchecked]:
            return Qt.PartiallyChecked
        elif check[Qt.Checked]:
            return Qt.Checked
        return Qt.Unchecked

    def childChecked(self, child, column, status):
        """Child was checked."""
        self._status[status].add(child.myhash)
        left = self._status.keys() - {status, }
        for sts in left:
            self._status[sts].discard(child.myhash)

        mystate = self.checkState(column)
        if status == Qt.PartiallyChecked:
            status = Qt.PartiallyChecked
        elif status != mystate:
            status = self._check_children()
        else:
            status = mystate

        super().setData(column, Qt.CheckStateRole, status)
        if isinstance(self.parent(), QTreeItem):
            self.parent().childChecked(self, column, status)


class PVNameTree(QTreeWidget):
    """Build a tree with SiriusPVNames."""

    itemChecked = Signal(QTreeItem, int, int)

    class BuildTree(QThread):
        """QThread to build tree."""

        itemInserted = Signal()

        def __init__(self, obj):
            """Init."""
            super().__init__(obj)
            self.obj = obj
            self._quit_task = False

        def size(self):
            """Return task size."""
            return len(self.obj.items)

        def exit_task(self):
            """Set flag to quit thread."""
            self._quit_task = True

        def run(self):
            """Build tree."""
            leng = len(self.obj.items)
            curr = 0
            for itr, item in enumerate(self.obj.items):
                if self._quit_task:
                    break
                self.obj._add_item(item)
                pct = int(itr/leng*100)
                if pct >= curr:
                    curr = pct + 1
                    self.itemInserted.emit()

            self.finished.emit()

    def __init__(self, items=tuple(), tree_levels=tuple(),
                 checked_levels=tuple(), parent=None):
        """Constructor."""
        super().__init__(parent)

        self._item_map = dict()

        self._items = items
        self._pnames = tree_levels
        self._leafs = list()

        self._setup_ui()
        self._create_actions()

        self.setHeaderHidden(False)
        self.setHeaderLabels(['PVName', 'Value', 'Delay'])

        self.check_children = True
        self.check_parent = True

        self.check_requested_levels(checked_levels)

    def _setup_ui(self):
        self._add_items()
        self.expanded.connect(
            lambda idx: self.resizeColumnToContents(idx.column()))

    def _create_actions(self):
        self._act_check_all = QAction("Check All", self)
        self._act_check_all.triggered.connect(self.check_all)
        self._act_uncheck_all = QAction("Uncheck All", self)
        self._act_uncheck_all.triggered.connect(self.uncheck_all)
        self._act_expand_all = QAction("Expand All", self)
        self._act_expand_all.triggered.connect(self.expand_all)
        self._act_collapse_all = QAction("Collapse All", self)
        self._act_collapse_all.triggered.connect(lambda: self.collapseAll())

    def clear(self):
        """Clear tree."""
        self._items = tuple()
        self._leafs = list()
        self._item_map = dict()
        super().clear()

    @property
    def items(self):
        """Items."""
        return self._items

    @items.setter
    def items(self, value):
        self.clear()
        self._items = value
        self._add_items()

    def check_all(self):
        """Check all items."""
        for item in self._leafs:
            if not item.isHidden():
                item.setCheckState(0, Qt.Checked)

    def uncheck_all(self):
        """Uncheck all items."""
        for item in self._leafs:
            if not item.isHidden():
                item.setCheckState(0, Qt.Unchecked)

    def expand_all(self):
        """Expand all items."""
        for item in self._item_map.values():
            if item.childCount() > 0:
                item.setExpanded(True)

    @staticmethod
    def mag_group(name):
        """Return magnet group."""
        if re.match('^B\w*(-[0-9])?$', name.dev):
            return 'Dipole'
        elif re.match('^Q[A-RT-Z0-9]\w*(-[0-9])?$', name.dev):
            return 'Quadrupole'
        elif re.match('^QS.*$', name.dev):
            return 'Quadrupole Skew'
        elif re.match('^Spect.*$', name.dev):
            return 'Spetrometer'
        elif re.match('^Slnd.*$', name.dev):
            return 'Solenoid'
        elif re.match('^S\w*(-[0-9])?$', name.dev):
            return 'Sextupole'
        elif re.match('^C(H|V)(-[0-9])?$', name.dev):
            return 'Corrector'
        elif re.match('^FC\w*(-[0-9])?$', name.dev):
            return 'Fast Corrector'
        elif re.match('(Inj|Eje).*$', name.dev):
            return 'Pulsed'
        elif re.match('^Lens.*$', name.dev):
            return 'Lens'
        else:
            return 'Other'

    def check_requested_levels(self, levels):
        """Set requested levels checked."""
        for level in levels:
            self._item_map[level].setCheckState(0, Qt.Checked)

    def _add_item(self, item):

        if isinstance(item, str):
            pvname = item
            row = [item, ]
        else:
            if not isinstance(item[0], str):
                raise ValueError
            pvname = item[0]
            row = [item[0], ]
            row.extend([str(i) for i in item[1:]])
        # pvals = []
        parent = self.invisibleRootItem()
        parent_key = ''
        # if pvname.count(':') == 2 and pvname.count('-') == 3:
        try:
            pvname = SiriusPVName(pvname)
        except (IndexError, ValueError):
            pass
        # Deal with LI LLRF PVs:
        if pvname.startswith('LA'):
            dic_ = {'sec': 'LI', 'dis': 'RF', 'dev': 'LLRF'}
            for p in self._pnames:
                key = dic_.get(p, 'DLLRF')
                if key:
                    item_key = parent_key + key
                    # item = self._item_map.symbol(item_key)
                    item = self._item_map[item_key] \
                        if item_key in self._item_map else None
                    if item is not None:
                        parent = item
                    else:
                        new_item = QTreeItem([key], parent)
                        new_item.setCheckState(0, Qt.Unchecked)
                        # self._item_map.add_symbol(item_key, new_item)
                        self._item_map[item_key] = new_item
                        # parent.addChild(new_item)
                        parent = new_item
                    parent_key = item_key
        # Deal with BO LLRF PVs:
        elif pvname.startswith('BR'):
            dic_ = {'sec': 'BO', 'dis': 'RF', 'dev': 'DLLRF'}
            for p in self._pnames:
                key = dic_.get(p, 'DLLRF')
                if key:
                    item_key = parent_key + key
                    # item = self._item_map.symbol(item_key)
                    item = self._item_map[item_key] \
                        if item_key in self._item_map else None
                    if item is not None:
                        parent = item
                    else:
                        new_item = QTreeItem([key], parent)
                        new_item.setCheckState(0, Qt.Unchecked)
                        # self._item_map.add_symbol(item_key, new_item)
                        self._item_map[item_key] = new_item
                        # parent.addChild(new_item)
                        parent = new_item
                    parent_key = item_key
        elif isinstance(pvname, SiriusPVName):
            # Parse it with SiriusPVName
            pvname = SiriusPVName(pvname)
            # Parse PVName
            for p in self._pnames:
                try:
                    key = getattr(pvname, p)
                except AttributeError:
                    key = getattr(PVNameTree, p)(pvname)
                if key:
                    item_key = parent_key + key
                    # item = self._item_map.symbol(item_key)
                    item = self._item_map[item_key] \
                        if item_key in self._item_map else None
                    if item is not None:
                        parent = item
                    else:
                        new_item = QTreeItem([key], parent)
                        new_item.setCheckState(0, Qt.Unchecked)
                        # self._item_map.add_symbol(item_key, new_item)
                        self._item_map[item_key] = new_item
                        # parent.addChild(new_item)
                        parent = new_item
                    parent_key = item_key
        else:
            key = pvname[:2]
            item_key = parent_key + key
            item = self._item_map[item_key] \
                if item_key in self._item_map else None
            if item is None:
                new_item = QTreeItem([key], parent)
                new_item.setCheckState(0, Qt.Unchecked)
                self._item_map[item_key] = new_item
                parent = new_item
            else:
                parent = item
        # Insert leaf node pvname
        new_item = QTreeItem(row, parent)
        new_item.setCheckState(0, Qt.Unchecked)
        self._item_map[pvname] = new_item
        self._leafs.append(new_item)

    def _add_items(self):
        # Connect signals
        t = self.BuildTree(self)
        t.finished.connect(t.deleteLater)
        dlg = None
        # if len(self.items) > 1500:
        dlg = QProgressDialog(
            labelText='Building Tree',
            minimum=0, maximum=100, parent=self)
        t.itemInserted.connect(lambda: dlg.setValue(dlg.value() + 1))
        t.finished.connect(dlg.close)
        # Start
        t.start()
        if dlg and len(self._items) > 0:
            dlg.exec_()

    def checked_items(self):
        """Return checked items."""
        return [item.data(0, Qt.DisplayRole) for item in self._leafs
                if item.checkState(0) == Qt.Checked]

    def sizeHint(self):
        """Override sizehint."""
        return QSize(600, 600)

    def resizeEvent(self, event):
        """Resize Event."""
        self.setColumnWidth(0, self.width()*4/6)
        self.setColumnWidth(1, self.width()*1.5/6)
        self.setColumnWidth(2, self.width()*0.5/6)
        super().resizeEvent(event)

    def contextMenuEvent(self, event):
        """Show context menu."""
        menu = QMenu(self)
        menu.addAction(self._act_check_all)
        menu.addAction(self._act_uncheck_all)
        menu.addSeparator()
        menu.addAction(self._act_expand_all)
        menu.addAction(self._act_collapse_all)
        menu.popup(event.globalPos())

    def setData(self, index, role, value):
        print(index, role, value)
        super().setData(index, role, value)


if __name__ == "__main__":
    # import sys
    from siriushla.sirius_application import SiriusApplication

    app = SiriusApplication()

    items = []
    for i in range(800):
        items.extend([('SI-Fam:MA-B1B1{}:PwrState-Sel'.format(i), 1, 0.0),
                      ('BO-Fam:MA-QD{}:Current-SP'.format(i), 1, 0.0),
                      ('BO-Fam:MA-B-{}:PwrState-Sel'.format(i), 1, 0.0)])
    w = PVNameTree(items=items, tree_levels=('sec', 'mag_group'),
                   checked_levels=('BOQuadrupole', ))
    w.show()
    # w.items = items
    # w.check_requested_levels(('BOQuadrupole', ))

    # sys.exit(app.exec_())
    app.exec_()
