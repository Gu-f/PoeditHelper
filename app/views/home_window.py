from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem
from PySide6.QtCore import Qt, Signal, QRectF, QSize, QEasingCurve
from qfluentwidgets import ScrollArea, ListWidget, ComboBox, FlowLayout, PushButton, PrimaryPushButton, FluentIcon, IconWidget, PrimaryToolButton, TransparentToolButton


class TranslateInfoListWidget(QWidget):
    # 翻译列表
    def __init__(self):
        super().__init__()

        self.hBoxLayout = QHBoxLayout(self)
        self.listWidget = ListWidget(self)

        self.listWidget.setAlternatingRowColors(True)

        stands = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for stand in stands:
            item = QListWidgetItem(stand)
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.item_mouse_click)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.listWidget)
        # self.resize(300, 400)

    def item_mouse_click(self, item):
        print(item.text())


class TranslateSourceTargetSelectWidget(QWidget):

    def source_combo_box(self):
        comboBox = ComboBox()
        comboBox.addItems(self.combo_box_items)
        comboBox.setCurrentIndex(1)
        comboBox.setFixedWidth(100)
        comboBox.isFlat()
        return comboBox

    def target_combo_box(self):
        comboBox = ComboBox()
        comboBox.addItems(self.combo_box_items)
        comboBox.setCurrentIndex(0)
        comboBox.setFixedWidth(100)
        return comboBox

    def reverse_button(self):
        button = TransparentToolButton(FluentIcon.SYNC)
        button.clicked.connect(self.reverse_source_target)
        return button

    def reverse_source_target(self):
        s_temp_index = self.s_combo_box.currentIndex()
        self.s_combo_box.setCurrentIndex(self.t_combo_box.currentIndex())
        self.t_combo_box.setCurrentIndex(s_temp_index)

    def __init__(self):
        super().__init__()
        layout = FlowLayout(self, needAni=True)

        self.combo_box_items = ['zh', 'en']

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
        translate_list_widget = TranslateInfoListWidget()
        translate_source_target_widget = TranslateSourceTargetSelectWidget()

        self.vBoxLayout.addWidget(translate_source_target_widget)
        self.vBoxLayout.addWidget(translate_list_widget)
