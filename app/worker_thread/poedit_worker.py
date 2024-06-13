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
        if not self._poedit_app or not self._poedit_app.is_process_running():
            self._poedit_app = None
            self._top_window = None
            self.source_text_box = None
            self.target_text_box = None
            while True:
                try:
                    self._poedit_app = pywinauto.Application().connect(path="Poedit.exe")
                    break
                except Exception as e:
                    print("获取Poedit进程异常，疑似未打开app：", e)
                time.sleep(1)
        return self._poedit_app

    def get_top_window(self):
        if not self._top_window:
            self._top_window = self.get_poedit_app().window(found_index=0)
        return self._top_window

    def get_source_text_box(self):
        if not self.source_text_box:
            self.source_text_box = self.get_top_window().child_window(control_id=-31886)
        return self.source_text_box

    def get_target_text_box(self):
        if not self.target_text_box:
            self.target_text_box = self.get_top_window().child_window(control_id=-31875)
        return self.target_text_box

    def get_source_text(self):
        source_text_box = self.get_source_text_box()
        source_text = ""
        try:
            source_text = source_text_box.window_text()
        except Exception as e:
            print("待翻译文本获取异常，疑似未打开工程", e)
        return source_text

    def get_target_text(self):
        target_text_box = self.get_target_text_box()
        target_text = ""
        try:
            target_text = target_text_box.window_text()
        except Exception as e:
            print("待翻译文本获取异常，正在重试", e)
        return target_text

    def run(self):
        temp_content = ""
        while True:
            source_text = self.get_source_text()
            if self.get_poedit_app() and source_text != temp_content:
                temp_content = source_text
                self.poedit_listen.emit(temp_content)
            time.sleep(0.1)
