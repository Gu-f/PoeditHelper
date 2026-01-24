from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt, QEasingCurve
from qfluentwidgets import (
    ScrollArea,
    ListWidget,
    ComboBox,
    FlowLayout,
    FluentIcon,
    TransparentToolButton,
    BodyLabel,
)
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.views.main_window import MainWindow


class TranslateInfoListWidget(QWidget):
    # 翻译列表
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_widget: Optional[HomeInterface] = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.listWidget = ListWidget(self)

        self.listWidget.setAlternatingRowColors(True)

        self.listWidget.itemClicked.connect(self.item_mouse_click)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)
        # self.resize(300, 400)

    def list_add_item(self, item):
        self.listWidget.clear()
        list_item = QListWidgetItem(item)
        self.listWidget.addItem(list_item)

    def item_mouse_click(self, item):
        if not self.parent_widget or not self.parent_widget.parent_widget:
            return
        poedit_thread = self.parent_widget.parent_widget.poedit_thread
        poedit_thread.send_target_text(str(item.text()))


class TranslateSourceTargetSelectWidget(QWidget):
    def source_combo_box(self):
        comboBox = ComboBox()
        comboBox.setFixedWidth(100)
        comboBox.isFlat()
        return comboBox

    def target_combo_box(self):
        comboBox = ComboBox()
        comboBox.setFixedWidth(100)
        return comboBox

    def reverse_button(self):
        button = TransparentToolButton(FluentIcon.RIGHT_ARROW)
        button.clicked.connect(self.reverse_source_target)
        return button

    def reverse_source_target(self):
        s_index = self.s_combo_box.currentIndex()
        t_index = self.t_combo_box.currentIndex()
        if s_index < 0 or t_index < 0:
            return
        if t_index >= self.s_combo_box.count() or s_index >= self.t_combo_box.count():
            return
        self.s_combo_box.setCurrentIndex(t_index)
        self.t_combo_box.setCurrentIndex(s_index)

    def __init__(self):
        super().__init__()
        layout = FlowLayout(self, needAni=True)

        # 自定义动画
        layout.setAnimation(10, QEasingCurve.Type.OutQuad)

        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        self.s_combo_box = self.source_combo_box()
        self.reverse_button_var = self.reverse_button()
        self.t_combo_box = self.target_combo_box()

        layout.addWidget(self.s_combo_box)
        layout.addWidget(self.reverse_button_var)
        layout.addWidget(self.t_combo_box)

        self.resize(250, 300)


class HomeInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_widget: Optional["MainWindow"] = parent
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadContent()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("homeInterface")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

    def loadContent(self):
        self.model_status_label = BodyLabel("模型加载：等待开始…", self)
        self.translate_list_widget = TranslateInfoListWidget(self)
        self.translate_source_target_widget = TranslateSourceTargetSelectWidget()

        self.vBoxLayout.addWidget(self.model_status_label)
        self.vBoxLayout.addWidget(self.translate_source_target_widget)
        self.vBoxLayout.addWidget(self.translate_list_widget)

    def update_model_status(self, text: str):
        self.model_status_label.setText(text)
