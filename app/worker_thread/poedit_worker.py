# -*- coding:utf-8 -*-
from PySide6.QtCore import QObject, Signal, QThread

from app.services.poedit_client import PoeditClient


class PoeditWorkerThread(QObject):
    poedit_listen = Signal(str)

    def __init__(self, parent=None, poll_interval_ms: int = 100):
        super().__init__(parent)
        self._client = PoeditClient()
        self._running = True
        self._poll_interval_ms = max(20, int(poll_interval_ms))

    def stop(self):
        self._running = False

    def send_target_text(self, text: str):
        self._client.send_target_text(text)

    def run(self):
        temp_content = ""
        while self._running:
            source_text = self._client.get_source_text()
            if source_text and source_text != temp_content:
                temp_content = source_text
                self.poedit_listen.emit(temp_content)
            QThread.msleep(self._poll_interval_ms)
