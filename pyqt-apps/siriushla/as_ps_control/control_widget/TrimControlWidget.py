"""Widgets to control Trim Quadrupoles magnets."""
from siriushla.as_ps_control.control_widget.BasePSControlWidget import \
    BasePSControlWidget


class TrimControlWidget(BasePSControlWidget):
    """Class to control a Fam Quad from the Sirius section."""

    def __init__(self, trim, **kwargs):
        """Get trim name."""
        self._trim = trim
        super().__init__(**kwargs)

    def _getFilter(self):
        return {"sec": "SI", "sub": "\w{4}", "dev": self._trim}

    def _hasTrimButton(self):
        return True

    def _hasScrollArea(self):
        return True

    def _getGroups(self):
        return [('Trims (1-10)', "SI-(0\d|10)"),
                ('Trims (11-20)', "SI-(1[1-9]|20)")]
