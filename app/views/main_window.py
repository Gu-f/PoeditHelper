from PySide6.QtCore import QSize, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, SplashScreen, NavigationItemPosition
from qfluentwidgets import FluentIcon

from app.views.help_window import HelpInterface
from app.views.home_window import HomeInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        # 创建导航子页
        self.homeInterface = HomeInterface(self)
        self.helpInterface = HelpInterface(self)

        # 向导航栏添加项
        self.initNavigation()
        self.splashScreen.finish()

    def initWindow(self):
        self.resize(345, 500)
        self.setMinimumWidth(345)
        self.setMinimumHeight(500)
        self.setWindowIcon(QIcon('app/res/logo.png'))
        self.setWindowTitle('PoeditHelper')

        self.setMicaEffectEnabled(True)

        # 创建开屏动画
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def open_source(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Gu-f/PoeditHelper"))

    def initNavigation(self):
        # 添加导航选项卡
        # t = Translator()
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, self.tr('翻译'))
        self.addSubInterface(self.helpInterface, FluentIcon.HELP, self.tr('帮助'), position=NavigationItemPosition.BOTTOM)

        # 源代码页跳转
        self.navigationInterface.addItem(
            routeKey='price',
            icon=FluentIcon.GITHUB,
            text="Github",
            onClick=self.open_source,
            selectable=False,
            tooltip="Github",
            position=NavigationItemPosition.BOTTOM
        )
