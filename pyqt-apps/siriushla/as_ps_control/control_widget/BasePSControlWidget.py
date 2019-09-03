"""Base class for controlling a power supply."""
import re

from qtpy.QtCore import Qt, Slot, QLocale
from qtpy.QtWidgets import QWidget, QVBoxLayout, QGroupBox, \
    QGridLayout, QLabel, QHBoxLayout, QScrollArea, QLineEdit, QAction, \
    QMenu, QInputDialog, QFrame, QPushButton, QSplitter, \
    QSizePolicy as QSzPlcy
import qtawesome as qta
from siriuspy.search import PSSearch, MASearch
from ..SummaryWidgets import SummaryWidget, SummaryHeader, get_prop2label


class PSContainer(QWidget):

    def __init__(self, widget, parent=None):
        super().__init__(parent)
        # Works for PS or MA
        self._widget = widget
        self._name = widget.devname

        self._dclinks = list()
        if self._name == 'BO-Fam:MA-B':
            psnames = MASearch.conv_maname_2_psnames(self._name)
            for name in psnames:
                self._dclinks.extend(PSSearch.conv_psname_2_dclink(name))
        elif self._name != 'SI-Fam:MA-B1B2':
            psname = self._name.replace(':MA-', ':PS-')
            self._dclinks = PSSearch.conv_psname_2_dclink(psname)

        self._setup_ui()
        self._create_actions()
        self.setStyleSheet("""
            #HideButton {
                min-width: 10px;
                max-width: 10px;
            }
            #DCLinkContainer {
                background-color: lightgrey;
            }
        """)

    def _setup_ui(self):
        """Setup widget UI."""
        self._layout = QGridLayout()
        self._layout.setSpacing(10)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._dclink_container = QWidget(self)
        self._dclink_container.setObjectName('DCLinkContainer')
        self._dclink_container.setLayout(QVBoxLayout())
        if self._dclinks:
            visible_props = {'detail', 'state', 'intlk', 'setpoint', 'monitor'}
            self._dclink_container.layout().addWidget(
                SummaryHeader(self._dclinks[0], visible_props, self))
            for dclink_name in self._dclinks:
                w = SummaryWidget(dclink_name, visible_props, self)
                self._dclink_container.layout().addWidget(w)
            self._hide = QPushButton(qta.icon('mdi.plus'), '', self)
        else:
            self._hide = QPushButton('', self)
            self._hide.setEnabled(False)
        self._hide.setObjectName('HideButton')
        self._hide.setSizePolicy(QSzPlcy.Maximum, QSzPlcy.Maximum)
        self._hide.setFlat(True)

        self._layout.addWidget(self._hide, 0, 0, Qt.AlignCenter)
        self._layout.addWidget(self._widget, 0, 1)
        self._layout.addWidget(self._dclink_container, 1, 1)

        # Configure
        self._dclink_container.setHidden(True)
        self._hide.clicked.connect(self._toggle_dclink)

    def _toggle_dclink(self):
        if self._dclink_container.isHidden():
            self._hide.setIcon(qta.icon('mdi.minus'))
            self._dclink_container.setHidden(False)
        else:
            self._hide.setIcon(qta.icon('mdi.plus'))
            self._dclink_container.setHidden(True)

    # Action methods
    def _create_actions(self):
        self._turn_on_action = QAction('Turn DCLinks On', self)
        self._turn_on_action.triggered.connect(
            lambda: self._set_dclink_pwrstate(True))
        self._turn_off_action = QAction('Turn DCLinks Off', self)
        self._turn_off_action.triggered.connect(
            lambda: self._set_dclink_pwrstate(False))
        self._open_loop_action = QAction('Open DCLinks Control Loop', self)
        self._open_loop_action.triggered.connect(
            lambda: self._set_dclink_control_loop(False))
        self._close_loop_action = QAction('Close DCLinks Control Loop', self)
        self._close_loop_action.triggered.connect(
            lambda: self._set_dclink_control_loop(True))
        self._set_setpoint_action = QAction('Set DCLinks Voltage', self)
        self._set_setpoint_action.triggered.connect(self._set_setpoint)
        self._reset_intlk_action = QAction('Reset DCLinks Interlocks', self)

    def _set_dclink_pwrstate(self, value):
        for dclink in self.dclink_widgets():
            btn = dclink.state_btn
            if value:
                if not btn._bit_val:
                    btn.send_value()
            else:
                if btn._bit_val:
                    btn.send_value()

    def _set_dclink_control_loop(self, value):
        for dclink in self.dclink_widgets():
            btn = dclink.control_btn
            if value:
                if btn._bit_val:
                    btn.send_value()
            else:
                if not btn._bit_val:
                    btn.send_value()

    def _set_setpoint(self):
        """Set current setpoint for every visible widget."""
        dlg = QInputDialog(self)
        dlg.setLocale(QLocale(QLocale.English))
        new_value, ok = dlg.getDouble(
            self, "New setpoint", "Value")
        if ok:
            for dclink in self.dclink_widgets():
                sp = dclink.setpoint.sp_lineedit
                sp.setText(str(new_value))
                try:
                    sp.send_value()
                except TypeError:
                    pass

    def _reset_intlk(self):
        for dclink in self.dclink_widgets():
            dclink.reset.click()

    # Overloaded method
    def contextMenuEvent(self, event):
        """Overload to create a custom context menu."""
        widget = self.childAt(event.pos())
        parent = widget.parent()
        grand_parent = parent.parent()
        if widget.objectName() == 'DCLinkContainer' or \
                parent.objectName() == 'DCLinkContainer' or \
                grand_parent.objectName() == 'DCLinkContainer':
            menu = QMenu(self)
            menu.addAction(self._turn_on_action)
            menu.addAction(self._turn_off_action)
            menu.addSeparator()
            menu.addAction(self._close_loop_action)
            menu.addAction(self._open_loop_action)
            menu.addSeparator()
            menu.addAction(self._set_setpoint_action)
            menu.addSeparator()
            menu.addAction(self._reset_intlk_action)
            menu.popup(event.globalPos())
        else:
            super().contextMenuEvent(event)


class BasePSControlWidget(QWidget):
    """Base widget class to control power supply."""

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, dev_type, orientation=0, parent=None):
        """Class constructor.

        Parameters:
        psname_list - a list of power supplies, will be filtered based on
                      patterns defined in the subclass;
        orientation - how the different groups(defined in subclasses) will be
                      laid out.
        """
        super(BasePSControlWidget, self).__init__(parent)
        self._orientation = orientation

        self._dev_type = dev_type
        if dev_type == 'PS':
            self._dev_list = PSSearch.get_psnames(self._getFilter())
        elif dev_type == 'MA':
            self._dev_list = MASearch.get_manames(self._getFilter())
        else:
            raise ValueError("Invalid device type, must be either PS or MA.")

        self.all_props = get_prop2label(self._dev_list[0])
        self.visible_props = {
            'detail', 'state', 'intlk', 'setpoint', 'monitor'}
        if 'psconn' in self.all_props:
            self.visible_props.update(
                ['psconn', 'strength_sp', 'strength_mon'])
        if 'trim' in self.all_props:
            self.visible_props.update(['trim', ])

        # Data used to filter the widgets
        self.ps_widgets_dict = dict()
        self.containers_dict = dict()
        self.filtered_widgets = set()  # Set with key of visible widgets

        # Setup the UI
        self.groups = self._getGroups()
        self._setup_ui()
        self._create_actions()
        if len(self.groups) in [1, 3]:
            self.setObjectName('cw')
            self.setStyleSheet('#cw{min-height: 40em;}')

    def _setup_ui(self):
        self.layout = QVBoxLayout()

        # Create filters
        self.search_le = QLineEdit(parent=self)
        self.search_le.setObjectName("search_lineedit")
        self.search_le.setPlaceholderText("Search for a power supply...")
        self.search_le.textEdited.connect(self._filter_pwrsupplies)
        self.filter_pb = QPushButton(qta.icon('mdi.view-column'), '', self)
        self.search_menu = QMenu(self.filter_pb)
        self.filter_pb.setMenu(self.search_menu)
        for prop, label in self.all_props.items():
            act = self.search_menu.addAction(label)
            act.setObjectName(prop)
            act.setCheckable(True)
            act.setChecked(prop in self.visible_props)
            act.toggled.connect(self._set_widgets_visibility)
        hlay_filter = QHBoxLayout()
        hlay_filter.addWidget(self.search_le)
        hlay_filter.addWidget(self.filter_pb)
        self.layout.addLayout(hlay_filter)

        self.count_label = QLabel(parent=self)
        self.count_label.setSizePolicy(QSzPlcy.Maximum, QSzPlcy.Maximum)
        self.layout.addWidget(self.count_label)

        self.pwrsupplies_layout = self._getSplitter()
        self.layout.addWidget(self.pwrsupplies_layout)
        if len(self.groups) == 3:
            splitt_v = QSplitter(Qt.Vertical)

        # Build power supply Layout
        # Create group boxes and pop. layout
        for idx, group in enumerate(self.groups):

            # Get power supplies that belong to group
            pwrsupplies = list()
            pattern = re.compile(group[1])
            for el in self._dev_list:
                if pattern.search(el):
                    pwrsupplies.append(el)

            # Create header
            header = SummaryHeader(pwrsupplies[0],
                                   visible_props=self.visible_props,
                                   parent=self)
            self.containers_dict['header '+group[0]] = header
            self.filtered_widgets.add('header '+group[0])

            # Loop power supply to create all the widgets of a groupbox
            group_widgets = list()
            for n, psname in enumerate(pwrsupplies):
                ps_widget = SummaryWidget(name=psname,
                                          visible_props=self.visible_props,
                                          parent=self)
                pscontainer = PSContainer(ps_widget, self)
                group_widgets.append(pscontainer)
                self.containers_dict[psname] = pscontainer
                self.filtered_widgets.add(psname)
                self.ps_widgets_dict[psname] = ps_widget

            # Create group
            group_box = self._createGroupBox(group[0], header, group_widgets)

            # Add group box to grid layout
            if len(self.groups) == 3:
                if idx in [0, 1]:
                    splitt_v.addWidget(group_box)
                else:
                    self.pwrsupplies_layout.addWidget(splitt_v)
                    self.pwrsupplies_layout.addWidget(group_box)
            else:
                self.pwrsupplies_layout.addWidget(group_box)

        self.count_label.setText(
            "Showing {} power supplies.".format(
                len(self.filtered_widgets)-len(self.groups)))
        self.setLayout(self.layout)

    def _createGroupBox(self, title, header, widget_group):
        scr_area_wid = QWidget(self)
        scr_area_wid.setObjectName('scr_ar_wid')
        scr_area_wid.setStyleSheet(
            '#scr_ar_wid {background-color: transparent;}')
        w_lay = QVBoxLayout(scr_area_wid)
        w_lay.setSpacing(0)
        w_lay.setContentsMargins(0, 0, 0, 0)
        for line, widget in enumerate(widget_group):
            w_lay.addWidget(widget, alignment=Qt.AlignLeft)
        w_lay.addStretch()

        min_width = '38' if self._dev_type == 'PS' else '54'
        scr_area = QScrollArea(self)
        scr_area.setObjectName('scr_area')
        scr_area.setStyleSheet('#scr_area{min-width: '+min_width+'em;}')
        scr_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scr_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scr_area.setWidgetResizable(True)
        scr_area.setFrameShape(QFrame.NoFrame)
        scr_area.setWidget(scr_area_wid)

        group_box = QGroupBox(title, parent=self)
        gb_lay = QVBoxLayout(group_box)
        gb_lay.addWidget(header, alignment=Qt.AlignLeft)
        gb_lay.addWidget(scr_area)
        return group_box

    def _getSplitter(self):
        if self._orientation == self.HORIZONTAL:
            return QSplitter(Qt.Horizontal)
        else:
            return QSplitter(Qt.Vertical)

    def _filter_pwrsupplies(self, text):
        """Filter power supply widgets based on text inserted at line edit."""
        try:
            pattern = re.compile(text, re.I)
        except Exception:  # Ignore malformed patterns?
            pattern = re.compile("malformed")

        # Clear filtered widgets and add the ones that match the new pattern
        self.filtered_widgets.clear()
        for name in self.containers_dict.keys():
            if pattern.search(name) or 'header' in name:
                self.filtered_widgets.add(name)

        # Set widgets visibility and the number of widgets matched
        self._set_widgets_visibility()
        self.count_label.setText(
            "Showing {} power supplies".format(
                len(self.filtered_widgets)-len(self.groups)))

        # Scroll to top
        for scroll_area in self.findChildren(QScrollArea):
            scroll_area.verticalScrollBar().setValue(0)

    def _set_widgets_visibility(self):
        """Set visibility of the widgets."""
        props = {act.objectName() for act in self.search_menu.actions()
                 if act.isChecked()}
        for key, wid in self.containers_dict.items():
            if 'header' in key:
                for ob in wid.findChildren(QWidget):
                    name = ob.objectName()
                    ob.setVisible(name in props or 'Hidden' in name)
            else:
                vis = key in self.filtered_widgets
                wid.setVisible(vis)
                if not vis:
                    continue
                objs = wid.findChildren(SummaryWidget)
                objs.extend(wid.findChildren(SummaryHeader))
                for ob in objs:
                    chil = ob.findChildren(
                        QWidget, options=Qt.FindDirectChildrenOnly)
                    for c in chil:
                        name = c.objectName()
                        c.setVisible(name in props)

    # Actions methods
    def _create_actions(self):
        self.turn_on_act = QAction("Turn On", self)
        self.turn_on_act.triggered.connect(lambda: self._set_pwrstate(True))

        self.turn_off_act = QAction("Turn Off", self)
        self.turn_off_act.triggered.connect(lambda: self._set_pwrstate(False))

        self.set_slowref_act = QAction("Set OpMode to SlowRef", self)
        self.set_slowref_act.triggered.connect(self._set_slowref)

        self.set_current_sp_act = QAction("Set Current SP", self)
        self.set_current_sp_act.triggered.connect(self._set_current_sp)

        self.reset_act = QAction("Reset Interlocks", self)
        self.reset_act.triggered.connect(self._reset_interlocks)

    @Slot(bool)
    def _set_pwrstate(self, state):
        """Execute turn on/off actions."""
        for key, widget in self.ps_widgets_dict.items():
            if key in self.filtered_widgets:
                try:
                    if state:
                        widget.turn_on()
                    else:
                        widget.turn_off()
                except TypeError:
                    pass

    @Slot()
    def _set_slowref(self):
        """Set opmode to SlowRef for every visible widget."""
        for key, widget in self.ps_widgets_dict.items():
            if key in self.filtered_widgets:
                try:
                    widget.set_opmode_slowref()
                except TypeError:
                    pass

    @Slot()
    def _set_current_sp(self):
        """Set current setpoint for every visible widget."""
        dlg = QInputDialog(self)
        dlg.setLocale(QLocale(QLocale.English))
        new_value, ok = dlg.getDouble(
            self, "Insert current setpoint", "Value")
        if ok:
            for key, widget in self.ps_widgets_dict.items():
                if key in self.filtered_widgets:
                    widget.setpoint.sp_lineedit.setText(str(new_value))
                    try:
                        widget.setpoint.sp_lineedit.send_value()
                    except TypeError:
                        pass

    @Slot()
    def _reset_interlocks(self):
        """Reset interlocks."""
        for key, widget in self.ps_widgets_dict.items():
            if key in self.filtered_widgets:
                try:
                    widget.reset()
                except TypeError:
                    pass

    # Overloaded method
    def contextMenuEvent(self, event):
        """Show a custom context menu."""
        point = event.pos()
        menu = QMenu("Actions", self)
        menu.addAction(self.turn_on_act)
        menu.addAction(self.turn_off_act)
        menu.addAction(self.set_slowref_act)
        menu.addAction(self.set_current_sp_act)
        menu.addAction(self.reset_act)
        menu.popup(self.mapToGlobal(point))

    def get_summary_widgets(self):
        """Return Summary Widgets."""
        return self.findChildren(SummaryWidget)
