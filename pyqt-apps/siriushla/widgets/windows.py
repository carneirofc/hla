"""Sirius Windows module."""
from qtpy.QtGui import QKeySequence
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QDialog, QHBoxLayout, QApplication, \
    QWidget, QLabel
import pyqtgraph as pg
from siriushla.util import get_package_version


def _create_siriuswindow(qt_type):
    """Create a _SiriusWindow that inherits from qt_type."""
    class _SiriusWindow(qt_type):
        """Auxiliar _SiriusWindow class.

        Parameters
        ----------
        parent : QWidget
            The parent widget for the SiriusMainWindow
        """

        Stylesheet = ""
        FontSizeSS = "* {{font-size: {}pt;}}"

        def __init__(self, *args, **kwargs):
            """Init."""
            super().__init__(*args, **kwargs)
            self.setFocus(True)
            self.app = QApplication.instance()
            if isinstance(self, SiriusMainWindow):
                self.label_version = QLabel(
                    'siriushla version: ' + get_package_version(),
                    self, alignment=Qt.AlignRight)
                self.label_version.setStyleSheet('font-size: 6pt;')
                self.statusBar().addPermanentWidget(self.label_version)

        def keyPressEvent(self, event):
            """Override keyPressEvent."""
            font = self.app.font()
            if event.matches(QKeySequence.ZoomIn):
                font.setPointSize(font.pointSize() + 1)
                self.app.setFont(font)
                self.changeFontSize()
            elif event.matches(QKeySequence.ZoomOut) and font.pointSize() > 6:
                font.setPointSize(font.pointSize() - 1)
                self.app.setFont(font)
                self.changeFontSize()
            super().keyPressEvent(event)

        def changeFontSize(self):
            fontsize = self.app.font().pointSize()
            self.ensurePolished()
            for w in self.findChildren(QWidget):
                font = w.font()
                font.setPointSize(fontsize)
                w.setFont(font)
            self.adjustSize()

            # handle resizing of pyqtgraph plots labels
            fontsize_str = str(fontsize)+'pt'
            for w in self.findChildren(pg.PlotWidget):
                # axes labels
                for ax in w.getPlotItem().axes.values():
                    sty = ax['item'].labelStyle
                    sty['font-size'] = fontsize_str
                    ax['item'].setLabel(text=None, **sty)
                # legend
                if w.plotItem.legend:
                    legw = 0
                    for item in w.plotItem.legend.items:
                        item[1].opts['size'] = fontsize_str
                        item[1].setText(text=item[1].text, **item[1].opts)
                        legw = max(legw, 20+item[1].width())
                    w.plotItem.legend.updateSize()
                    w.plotItem.legend.setFixedWidth(legw)
                # title
                wtitle = w.plotItem.titleLabel
                wtitle.opts['size'] = fontsize_str
                wtitle.setText(text=wtitle.text, **wtitle.opts)
            for w in self.findChildren(pg.GraphicsLayoutWidget):
                sty = w.xaxis.labelStyle
                sty['font-size'] = fontsize_str
                w.xaxis.setLabel(text=None, **sty)
                sty = w.yaxis.labelStyle
                sty['font-size'] = fontsize_str
                w.yaxis.setLabel(text=None, **sty)

    return _SiriusWindow


SiriusMainWindow = _create_siriuswindow(QMainWindow)
SiriusDialog = _create_siriuswindow(QDialog)


def create_window_from_widget(WidgetClass, title='', icon=None, is_main=False):

    if is_main:
        class MyWindow(SiriusMainWindow):

            def __init__(self, parent, *args, **kwargs):
                super().__init__(parent)
                self.widget = WidgetClass(self, *args, **kwargs)
                self.setCentralWidget(self.widget)
                self.setWindowTitle(title)
                if icon:
                    self.setWindowIcon(icon)
                self.setObjectName(self.widget.objectName())
    else:
        class MyWindow(SiriusDialog):

            def __init__(self, parent, *args, **kwargs):
                super().__init__(parent)
                hbl = QHBoxLayout(self)
                self.widget = WidgetClass(self, *args, **kwargs)
                hbl.addWidget(self.widget)
                self.setWindowTitle(title)
                if icon:
                    self.setWindowIcon(icon)
                self.setObjectName(self.widget.objectName())

    MyWindow.__name__ = WidgetClass.__name__.replace('Widget', 'Window')
    return MyWindow
