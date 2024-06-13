from PySide6.QtCore import QSize, QUrl, QThread
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, SplashScreen, NavigationItemPosition
from qfluentwidgets import FluentIcon

from app.translate_core.tanslater import AITranslater
from app.views.help_window import HelpInterface
from app.views.home_window import HomeInterface
from app.worker_thread.poedit_worker import PoeditWorkerThread


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.temp_model_category = ""
        self.initWindow()
        # 创建导航子页
        self.homeInterface = HomeInterface(self)
        self.helpInterface = HelpInterface(self)

        # 向导航栏添加项
        self.initNavigation()
        self.splashScreen.finish()

        # 模型解包
        self.translator = self.unpack_translte_model()

        # 初始化线程
        self.init_thread()

        # 初始化模型数据到选择列表
        self.homeInterface.translate_source_target_widget.s_combo_box.addItems(self.translator.translate_models.source_items)
        self.homeInterface.translate_source_target_widget.t_combo_box.addItems(self.translator.translate_models.target_items)

    def unpack_translte_model(self):
        return AITranslater()

    def set_translate_model(self, category):
        if category != self.temp_model_category:
            self.homeInterface.translate_list_widget.list_add_item("切换模型中...")
            self.translator.translator = None
            self.translator.init_translater(category=category, device='cpu')
            self.temp_model_category = category

    def init_thread(self):
        self.thread = QThread()
        self.poedit_thread = PoeditWorkerThread()
        self.poedit_thread.moveToThread(self.thread)

        # 处理线程返回信号
        self.poedit_thread.poedit_listen.connect(self.poedit_action)

        # 启动线程
        self.thread.started.connect(self.poedit_thread.run)
        self.thread.start()

    def poedit_action(self, translate_text):
        s = self.homeInterface.translate_source_target_widget.s_combo_box.text()
        t = self.homeInterface.translate_source_target_widget.t_combo_box.text()
        category = f"{s}_{t}"
        self.set_translate_model(category)
        translate_result = self.translator.ai_translate(translate_text)
        self.homeInterface.translate_list_widget.list_add_item(translate_result)

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
        self.addSubInterface(self.helpInterface, FluentIcon.HELP, self.tr('帮助'),
                             position=NavigationItemPosition.BOTTOM)

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
