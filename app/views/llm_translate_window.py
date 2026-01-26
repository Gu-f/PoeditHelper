from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem
from qfluentwidgets import ScrollArea, ListWidget, ComboBox, BodyLabel


TARGET_LANGUAGES = [
    "中文（简体）",
    "中文（繁体）",
    "英语",
    "日语",
    "韩语",
    "法语",
    "德语",
    "西班牙语",
    "俄语",
    "葡萄牙语",
    "意大利语",
]

if TYPE_CHECKING:
    from app.views.main_window import MainWindow


class LlmTranslateListWidget(QWidget):
    # LLM 翻译结果列表
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_widget: Optional[LlmTranslateInterface] = parent

        self.h_box_layout = QHBoxLayout(self)
        self.list_widget = ListWidget(self)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemClicked.connect(self.item_mouse_click)

        self.h_box_layout.setContentsMargins(0, 0, 0, 0)
        self.h_box_layout.addWidget(self.list_widget)

    def list_add_item(self, item: str):
        self.list_widget.clear()
        list_item = QListWidgetItem(item)
        self.list_widget.addItem(list_item)

    def item_mouse_click(self, item):
        if not self.parent_widget or not self.parent_widget.parent_widget:
            return
        poedit_thread = self.parent_widget.parent_widget.poedit_thread
        poedit_thread.send_target_text(str(item.text()))


class LlmTargetSelectWidget(QWidget):
    # 仅选择目标语言
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.target_combo_box = ComboBox(self)
        self.target_combo_box.setFixedWidth(160)
        self.target_combo_box.addItems(TARGET_LANGUAGES)

        layout.addWidget(BodyLabel("目标语言：", self))
        layout.addWidget(self.target_combo_box)
        layout.addStretch(1)


class LlmTranslateInterface(ScrollArea):
    """LLM 翻译页面"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_widget: Optional["MainWindow"] = parent
        self.view = QWidget(self)
        self.v_box_layout = QVBoxLayout(self.view)

        self.__init_widget()
        self.load_content()

    def __init_widget(self):
        self.view.setObjectName("view")
        self.setObjectName("llmTranslateInterface")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

    def load_content(self):
        self.model_status_label = BodyLabel("LLM 状态：等待请求", self)
        self.target_select_widget = LlmTargetSelectWidget()
        self.translate_list_widget = LlmTranslateListWidget(self)

        self.v_box_layout.addWidget(self.model_status_label)
        self.v_box_layout.addWidget(self.target_select_widget)
        self.v_box_layout.addWidget(self.translate_list_widget)

    def update_status(self, text: str):
        self.model_status_label.setText(text)

    def get_target_language(self) -> str:
        return self.target_select_widget.target_combo_box.currentText()
