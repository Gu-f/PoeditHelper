# -*- coding:utf-8 -*-
from PySide6.QtCore import QObject, Signal, Slot

from app.translate_core.tanslater import AITranslater
from app.services.translator_cache import TranslatorCache


class TranslateWorker(QObject):
    translated = Signal(str)
    models_ready = Signal(list, list)
    loading_status = Signal(str)

    def __init__(self, cache: TranslatorCache, parent=None):
        super().__init__(parent)
        self._translator = None
        self._current_category = ""
        self._translator_cache = cache

    @Slot()
    def initialize(self):
        self._translator = AITranslater()
        source_items = self._translator.translate_models.get_source_items()
        target_items = self._translator.translate_models.get_target_items()
        self.models_ready.emit(source_items, target_items)

    @Slot(str, str)
    def translate(self, text: str, category: str):
        if not self._translator:
            self.initialize()
        translator = self._translator
        if not translator:
            self.translated.emit("未检测到有效的翻译模型")
            return
        if category:
            cached = self._translator_cache.get(category)
            if cached:
                self._current_category = category
                result = cached.translate(text)
                self.translated.emit(result)
                return
            if category != self._current_category:
                self._load_category(category)
        if category and self._current_category != category:
            self.translated.emit("未检测到有效的翻译模型")
            return
        active = self._translator_cache.get(self._current_category)
        if not active:
            self.translated.emit("未检测到有效的翻译模型")
            return
        result = active.translate(text)
        self.translated.emit(result)

    def _load_category(self, category: str):
        translator = self._translator
        if not translator or not category:
            return
        if self._translator_cache.has(category):
            self._current_category = category
            self.loading_status.emit(f"模型已加载：{category}")
            return
        self.loading_status.emit(f"模型加载中：{category}")
        translator.translator = None
        translator.init_translater(category=category, device="cpu")
        package_translator = translator.translator
        if package_translator:
            self._translator_cache.set(category, package_translator)
            self._current_category = category
        self.loading_status.emit("模型加载完成")
