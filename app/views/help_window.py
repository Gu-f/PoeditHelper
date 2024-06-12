from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import ScrollArea, TextEdit


class HelpInterface(ScrollArea):
    """ Help interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadContent()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('helpInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

    def loadContent(self):
        with open('README.MD', 'r', encoding='utf-8') as file:
            readme_md = file.read()
        textEdit = TextEdit(self)
        textEdit.setReadOnly(True)
        textEdit.setMarkdown(readme_md)
        self.vBoxLayout.addWidget(textEdit)
