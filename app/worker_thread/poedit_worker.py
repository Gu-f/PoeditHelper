# -*- coding:utf-8 -*-
import time
import pywinauto

from PySide6.QtCore import QObject, Signal


class PoeditWorkerThread(QObject):
    poedit_listen = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._poedit_app = None
        self._top_window = None
        self.source_text_box = None
        self.target_text_box = None

    def get_poedit_app(self):
        if not self._poedit_app:
            self._poedit_app = pywinauto.Application().connect(path="Poedit.exe")
        return self._poedit_app

    def get_source_text_box(self):
        if not self.source_text_box:
            self.source_text_box = self.get_poedit_app().window(found_index=0).child_window(control_id=-31886)
        return self.source_text_box

    def get_target_text_box(self):
        if not self.target_text_box:
            self.target_text_box = self.get_poedit_app().window(found_index=0).child_window(control_id=-31875)
        return self.target_text_box

    def run(self):
        temp_content = ""
        while True:
            if self.get_source_text_box().window_text() != temp_content:
                temp_content = self.get_source_text_box().window_text()
                self.poedit_listen.emit(temp_content)
            time.sleep(0.1)
