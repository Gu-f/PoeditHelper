# -*- coding:utf-8 -*-
from PySide6.QtCore import QObject, Signal, Slot

from app.services.llm_client import LlmClient


class LlmTranslateWorker(QObject):
    translated = Signal(str)
    loading_status = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._client = LlmClient()

    @Slot(str, str, dict)
    def translate(self, text: str, target_language: str, config: dict):
        if not text or not text.strip():
            return
        self.loading_status.emit("LLM 翻译中...")
        result = self._client.translate(text, target_language, config)
        if result.startswith("LLM 请求失败") or result.startswith("请先配置") or result.startswith("LLM 响应解析失败"):
            self.loading_status.emit(result)
        else:
            self.loading_status.emit("LLM 翻译完成")
        if result:
            self.translated.emit(result)
