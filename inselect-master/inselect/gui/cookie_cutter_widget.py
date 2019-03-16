from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QAction, QFileDialog, QMenu

from inselect.lib.cookie_cutter import CookieCutter
from inselect.lib.utils import debug_print

from .cookie_cutter_choice import cookie_cutter_choice
from .utils import load_icon, reveal_path


class CookieCutterWidget(QObject):
    """Button that shows name of the currently selected cookie cutter and
    shows a popup menu when pressed.
    """

    FILE_FILTER = 'Inselect cookie cutter (*{0})'.format(
        CookieCutter.EXTENSION
    )

    def __init__(self, parent=None):
        super(CookieCutterWidget, self).__init__(parent)
        self._create_actions()
        self.popup = QMenu()
        self.inject_actions(self.popup)

    def _create_actions(self):
        self.save_to_new_action = QAction(
            "Save boxes to new cookie cutter...", self,
            icon=load_icon(':/icons/save.png')
        )
        self.choose_action = QAction(
            "Choose...", self, triggered=self.choose,
            icon=load_icon(':/icons/open.png')
        )
        self.reveal_action = QAction(
            "Reveal cookie cutter", self, triggered=self.reveal
        )
        self.clear_action = QAction(
            "Do not use a cookie cutter", self, triggered=self.clear,
            icon=load_icon(':/icons/close.png')
        )
        self.apply_current_action = QAction("Apply", self)

    def inject_actions(self, menu):
        "Adds cookie cutter actions to menu"
        menu.addAction(self.choose_action)
        menu.addAction(self.apply_current_action)
        menu.addAction(self.reveal_action)
        menu.addSeparator()
        menu.addAction(self.clear_action)
        menu.addSeparator()
        menu.addAction(self.save_to_new_action)

    def clear(self, checked=False):
        "Clears the choice of cookie cutter"
        cookie_cutter_choice().clear()

    def choose(self, checked=False):
        "Shows a 'choose cookie cutter' file dialog"
        debug_print('CookieCutterWidget.choose_cookie_cutter')
        path, selectedFilter = QFileDialog.getOpenFileName(
            None, "Choose cookie cutter",
            str(cookie_cutter_choice().last_directory()),
            self.FILE_FILTER
        )

        if path:
            # Save the user's choice
            cookie_cutter_choice().load(path)

    def reveal(self, checked=False):
        reveal_path(cookie_cutter_choice().current_path)

    def sync_ui(self, button, has_document, has_rows):
        "Sync state of actions"
        debug_print('CookieCutterWidget.sync_ui')
        current = cookie_cutter_choice().current
        has_current = cookie_cutter_choice().current is not None
        name = current.name if current else 'Cookie cutter'

        # Truncate text to fit button
        metrics = QFontMetrics(button.font())
        elided = metrics.elidedText(
            name, Qt.ElideRight, button.width() - 25
        )
        button.setText(elided)

        self.save_to_new_action.setEnabled(has_rows)
        self.clear_action.setEnabled(has_current)
        self.reveal_action.setEnabled(has_current)
        self.apply_current_action.setEnabled(has_document and has_current)
