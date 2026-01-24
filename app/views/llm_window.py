from __future__ import annotations

from typing import Dict, List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox
from qfluentwidgets import ScrollArea, ComboBox, LineEdit, SubtitleLabel, BodyLabel, isDarkTheme, qconfig


class LlmInterface(ScrollArea):
    """LLM 大模型翻译配置页"""

    # 系统提示词，限制只输出翻译内容并保持占位符不变
    SYSTEM_PROMPT = (
        "你是专业本地化翻译引擎。你的任务是把用户输入翻译成目标语言。\n"
        "只输出翻译后的字符串，不要添加解释或任何额外内容，不要使用代码块。\n"
        "保持占位符原样不变(例如 {name}、%s、%d、$VAR、{{placeholder}}等)。\n"
        "保持原文的换行与空白结构。"
    )

    # 提供商配置
    PROVIDERS: Dict[str, Dict[str, List[str] | str]] = {
        "Google AI Studio": {
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "models": [
                "gemini-3-flash-preview",
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-2.5-flash-preview-09-2025",
                "gemini-2.5-flash-lite",
                "gemini-2.5-flash-lite-preview-09-2025",
                "gemini-2.0-flash",
                "gemini-2.0-flash-lite",
            ],
        }
    }

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__init_widget()
        self.load_content()

    def __init_widget(self):
        self.view.setObjectName("view")
        self.setObjectName("llmInterface")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

    def load_content(self):
        title = SubtitleLabel("LLM 大模型翻译配置", self)
        desc = BodyLabel("大模型翻译相关配置", self)
        desc.setWordWrap(True)

        self.vBoxLayout.addWidget(title)
        self.vBoxLayout.addWidget(desc)

        self._build_basic_group()
        self._build_model_group()

        self.vBoxLayout.addStretch(1)

    def _build_basic_group(self):
        group = QGroupBox("基础配置", self)
        self._apply_group_style(group)
        layout = QFormLayout(group)

        self.proxy_input = LineEdit(group)
        self.proxy_input.setPlaceholderText("例如：http://127.0.0.1:7890")
        layout.addRow(BodyLabel("代理地址"), self.proxy_input)

        self.vBoxLayout.addWidget(group)

    def _build_model_group(self):
        group = QGroupBox("模型与接口", self)
        self._apply_group_style(group)
        layout = QFormLayout(group)

        self.provider_combo = ComboBox(group)
        self.provider_combo.addItems(list(self.PROVIDERS.keys()))
        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)
        layout.addRow(BodyLabel("模型提供商"), self.provider_combo)

        self.model_combo = ComboBox(group)
        layout.addRow(BodyLabel("模型选择"), self.model_combo)

        self.token_input = LineEdit(group)
        self.token_input.setEchoMode(LineEdit.EchoMode.Password)
        self.token_input.setPlaceholderText("请输入 API Token")
        layout.addRow(BodyLabel("Token"), self.token_input)

        self.openapi_input = LineEdit(group)
        self.openapi_input.setPlaceholderText("OpenAPI 基础地址")
        layout.addRow(BodyLabel("OpenAPI 地址"), self.openapi_input)

        self.provider_tip = BodyLabel("提供商切换后会自动填充默认地址和模型。", group)
        self.provider_tip.setWordWrap(True)
        layout.addRow(BodyLabel("提示"), self.provider_tip)

        self.vBoxLayout.addWidget(group)

        # 初始化提供商相关配置
        self._on_provider_changed(0)

    def _on_provider_changed(self, _index: int):
        provider_name = self.provider_combo.currentText()
        provider = self.PROVIDERS.get(provider_name, {})

        # 刷新模型列表与默认地址
        models = provider.get("models", [])
        self.model_combo.clear()
        self.model_combo.addItems(models)

        base_url_value = provider.get("base_url", "")
        base_url = base_url_value if isinstance(base_url_value, str) else ""
        self.openapi_input.setText(base_url)

    def _apply_group_style(self, group: QGroupBox):
        light_qss = (
            "QGroupBox{"
            "color:#000000;"
            "border:1px solid rgba(0,0,0,0.18);"
            "border-radius:6px;"
            "margin-top:12px;"
            "}"
            "QGroupBox::title{"
            "subcontrol-origin: margin;"
            "left:8px;"
            "padding:0 4px;"
            "}"
        )
        dark_qss = (
            "QGroupBox{"
            "color:#ffffff;"
            "border:1px solid rgba(255,255,255,0.25);"
            "border-radius:6px;"
            "margin-top:12px;"
            "}"
            "QGroupBox::title{"
            "subcontrol-origin: margin;"
            "left:8px;"
            "padding:0 4px;"
            "}"
        )

        def apply_style():
            group.setStyleSheet(dark_qss if isDarkTheme() else light_qss)

        apply_style()
        qconfig.themeChanged.connect(lambda *_: apply_style())

    def get_llm_config(self) -> Dict[str, str]:
        return {
            "provider": self.provider_combo.currentText(),
            "model": self.model_combo.currentText(),
            "api_key": self.token_input.text().strip(),
            "base_url": self.openapi_input.text().strip(),
            "proxy": self.proxy_input.text().strip(),
            "system_prompt": self.SYSTEM_PROMPT,
        }
