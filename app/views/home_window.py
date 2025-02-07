from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt, QEasingCurve
from qfluentwidgets import ScrollArea, ListWidget, ComboBox, FlowLayout, FluentIcon, TransparentToolButton

from app.utils import serializer_chars
from app.worker_thread.poedit_worker import PoeditWorkerThread


class TranslateInfoListWidget(QWidget):
    # 翻译列表
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.listWidget = ListWidget(self)

        self.listWidget.setAlternatingRowColors(True)

        self.listWidget.itemClicked.connect(self.item_mouse_click)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)
        # self.resize(300, 400)

    def list_add_item(self, item):
        self.listWidget.clear()
        item = QListWidgetItem(item)
        self.listWidget.addItem(item)

    def item_mouse_click(self, item):
        poedit_thread: PoeditWorkerThread = self.parent.parent.poedit_thread
        target_text_box = poedit_thread.get_target_text_box()
        target_text_box.send_chars(serializer_chars(str(item.text())))


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
        pass

    def __init__(self):
        super().__init__()
        layout = FlowLayout(self, needAni=True)

        # 自定义动画
        layout.setAnimation(10, QEasingCurve.OutQuad)

        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        self.s_combo_box = self.source_combo_box()
        self.reverse_button = self.reverse_button()
        self.t_combo_box = self.target_combo_box()

        layout.addWidget(self.s_combo_box)
        layout.addWidget(self.reverse_button)
        layout.addWidget(self.t_combo_box)

        self.resize(250, 300)
        self.setStyleSheet('Demo{background: white} QPushButton{padding: 5px 10px; font:15px "Microsoft YaHei"}')


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadContent()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

    def loadContent(self):
        self.translate_list_widget = TranslateInfoListWidget(self)
        self.translate_source_target_widget = TranslateSourceTargetSelectWidget()

        self.vBoxLayout.addWidget(self.translate_source_target_widget)
        self.vBoxLayout.addWidget(self.translate_list_widget)
