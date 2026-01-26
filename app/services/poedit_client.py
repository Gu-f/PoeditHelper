import logging
import time

from app.utils import serializer_chars


class PoeditClient:
    def __init__(
        self,
        app_path: str = "Poedit.exe",
        class_name: str = "RICHEDIT50W",
        source_index: int = 0,
        target_index: int = 1,
        connect_retry_s: float = 1.0,
    ):
        self._app_path = app_path
        self._class_name = class_name
        self._source_index = source_index
        self._target_index = target_index
        self._connect_retry_s = max(0.2, float(connect_retry_s))
        self._app = None
        self._top_window = None
        self._source_text_box = None
        self._target_text_box = None
        self._logger = logging.getLogger(__name__)

    def _reset_cache(self):
        self._app = None
        self._top_window = None
        self._source_text_box = None
        self._target_text_box = None

    def _connect(self):
        import pywinauto

        if self._app and self._app.is_process_running():
            return self._app
        self._reset_cache()
        try:
            self._app = pywinauto.Application().connect(path=self._app_path)
        except Exception as exc:
            self._logger.debug("Poedit connect failed: %s", exc)
            time.sleep(self._connect_retry_s)
            return None
        return self._app

    def _get_top_window(self):
        app = self._connect()
        if not app:
            return None
        if not self._top_window:
            try:
                self._top_window = app.window(found_index=0)
            except Exception as exc:
                self._logger.debug("Poedit window lookup failed: %s", exc)
                self._reset_cache()
                return None
        return self._top_window

    def _get_text_box(self, index: int):
        top = self._get_top_window()
        if not top:
            return None
        try:
            return top.child_window(class_name=self._class_name, found_index=index)
        except Exception as exc:
            self._logger.debug("Poedit textbox lookup failed: %s", exc)
            self._reset_cache()
            return None

    def get_source_text(self) -> str:
        box = self._get_text_box(self._source_index)
        if not box:
            return ""
        try:
            return box.window_text()
        except Exception as exc:
            self._logger.debug("Poedit source text read failed: %s", exc)
            self._reset_cache()
            return ""

    def send_target_text(self, text: str) -> None:
        box = self._get_text_box(self._target_index)
        if not box:
            return
        try:
            box.send_chars(serializer_chars(str(text)))
        except Exception as exc:
            self._logger.debug("Poedit target text send failed: %s", exc)
            self._reset_cache()
