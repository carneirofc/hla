"""Util module."""
import os as _os
import re as _re
import pathlib as _pathlib

from pydm.PyQt.QtCore import QFile as _QFile
import siriushla.resources as _resources


def set_style(app, force_default=False):
    """Implement sirius-hla-style.css as default Qt resource file HLA."""
    if force_default:
        stream = _QFile(':/sirius-hla-style.css')
    else:
        fname = str(_os.path.join(_pathlib.Path.home(),
                    '.sirius-hla-style.css'))
        fpath = _pathlib.Path(fname)
        if not fpath.is_file():
            fname = ':/sirius-hla-style.css'
        stream = _QFile(fname)
    if stream.open(_QFile.ReadOnly):
        style = str(stream.readAll(), 'utf-8')
        stream.close()
        app.setStyleSheet(style)
    else:
        print('set_style: "{0}": {1}'.format(fname, stream.errorString()))
    _resources.qCleanupResources()


def get_kick_unit(channel):
    if channel.find("SI-") > -1:
        section = "SI"
    elif channel.find("TS-") > -1:
        section = "TS"
    elif channel.find("BO-") > -1:
        section = "BO"
    elif channel.find("TB-") > -1:
        section = "TB"

    pvname = channel[channel.find(section):]

    if _re.search("-(CH|CV|FCH|FCV).*:", pvname):
        if section in ["SI", "BO"]:
            return "urad"
        elif section in ["TS", "TB"]:
            return "mrad"
    else:
        return "rad"
