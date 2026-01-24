from PySide6.QtCore import QSize, QUrl, QThread, Signal
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, SplashScreen, NavigationItemPosition
from qfluentwidgets import FluentIcon
from qfluentwidgets import Theme, setTheme, isDarkTheme

from app.views.help_window import HelpInterface
from app.views.home_window import HomeInterface
from app.views.llm_window import LlmInterface
from app.views.llm_translate_window import LlmTranslateInterface
from app.worker_thread.poedit_worker import PoeditWorkerThread
from app.worker_thread.translate_worker import TranslateWorker
from app.worker_thread.llm_translate_worker import LlmTranslateWorker
from app.services.translator_cache import TranslatorCache
from app.config import HelperConfig


class MainWindow(FluentWindow):
    request_translate = Signal(str, str)
    request_llm_translate = Signal(str, str, dict)

    def __init__(self):
        super().__init__()
        self.initWindow()
        # 创建导航子页
        self.homeInterface = HomeInterface(self)
        self.llmInterface = LlmInterface(self)
        self.llmTranslateInterface = LlmTranslateInterface(self)
        self.helpInterface = HelpInterface(self)

        # 向导航栏添加页面
        self.initNavigation()
        self.splashScreen.finish()

        # 初始化线程
        self.init_thread()

    def init_thread(self):
        self.q_thread = QThread()
        self.poedit_thread = PoeditWorkerThread()
        self.poedit_thread.moveToThread(self.q_thread)

        # 处理线程返回信号
        self.poedit_thread.poedit_listen.connect(self.poedit_action)

        # 启动线程
        self.q_thread.started.connect(self.poedit_thread.run)
        self.q_thread.start()

        self.translator_cache = TranslatorCache()

        self.translate_thread = QThread()
        self.translate_worker = TranslateWorker(self.translator_cache)
        self.translate_worker.moveToThread(self.translate_thread)
        self.translate_thread.started.connect(self.translate_worker.initialize)
        self.translate_worker.models_ready.connect(self._on_models_ready)
        self.translate_worker.translated.connect(self._on_translate_result)
        self.translate_worker.loading_status.connect(self._on_model_loading_status)
        self.request_translate.connect(self.translate_worker.translate)
        self.translate_thread.start()

        self.llm_translate_thread = QThread()
        self.llm_translate_worker = LlmTranslateWorker()
        self.llm_translate_worker.moveToThread(self.llm_translate_thread)
        self.llm_translate_worker.translated.connect(self._on_llm_translate_result)
        self.llm_translate_worker.loading_status.connect(self._on_llm_translate_status)
        self.request_llm_translate.connect(self.llm_translate_worker.translate)
        self.llm_translate_thread.start()

    def poedit_action(self, translate_text):
        s = self.homeInterface.translate_source_target_widget.s_combo_box.text()
        t = self.homeInterface.translate_source_target_widget.t_combo_box.text()
        category = f"{s}_{t}"
        self.request_translate.emit(translate_text, category)
        self._request_llm_translate(translate_text)

    def _on_models_ready(self, source_items, target_items):
        self.homeInterface.translate_source_target_widget.s_combo_box.addItems(source_items)
        self.homeInterface.translate_source_target_widget.t_combo_box.addItems(target_items)

    def _on_translate_result(self, translate_result):
        self.homeInterface.translate_list_widget.list_add_item(translate_result)

    def _on_model_loading_status(self, text):
        self.homeInterface.update_model_status(text)

    def _request_llm_translate(self, text: str):
        target_language = self.llmTranslateInterface.get_target_language()
        config = self.llmInterface.get_llm_config()
        if not target_language:
            self.llmTranslateInterface.update_status("LLM 翻译失败：未选择目标语言")
            return
        if not config.get("api_key") or not config.get("model") or not config.get("base_url"):
            self.llmTranslateInterface.update_status("LLM 翻译失败：请先配置模型与 Token")
            return
        self.request_llm_translate.emit(text, target_language, config)

    def _on_llm_translate_result(self, translate_result: str):
        self.llmTranslateInterface.translate_list_widget.list_add_item(translate_result)

    def _on_llm_translate_status(self, text: str):
        self.llmTranslateInterface.update_status(text)

    def initWindow(self):
        setTheme(Theme.AUTO)
        self.resize(400, 600)
        self.setMinimumWidth(350)
        self.setMinimumHeight(500)
        self.setWindowIcon(QIcon("app/res/logo.png"))
        self.setWindowTitle(f"PoeditHelper V{HelperConfig.VERSION}")

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

    def _get_theme_toggle_text(self):
        if isDarkTheme():
            return "切换到亮色模式"
        return "切换到暗色模式"

    def _update_theme_toggle_item(self):
        if hasattr(self, "themeToggleItem"):
            text = self._get_theme_toggle_text()
            self.themeToggleItem.setText(text)
            self.themeToggleItem.setToolTip(text)

    def toggle_theme(self):
        theme = Theme.LIGHT if isDarkTheme() else Theme.DARK
        setTheme(theme)
        self._update_theme_toggle_item()

    def initNavigation(self):
        # 添加导航选项卡
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, self.tr("翻译"))
        # 新增 LLM 翻译页面
        self.addSubInterface(self.llmTranslateInterface, FluentIcon.ROBOT, self.tr("LLM 翻译"))
        # 新增 LLM 翻译配置页面
        self.addSubInterface(
            self.llmInterface,
            FluentIcon.SETTING,
            self.tr("LLM 配置"),
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(
            self.helpInterface, FluentIcon.HELP, self.tr("帮助"), position=NavigationItemPosition.BOTTOM
        )

        # 源码页跳转
        self.navigationInterface.addItem(
            routeKey="price",
            icon=FluentIcon.GITHUB,
            text="Github",
            onClick=self.open_source,
            selectable=False,
            tooltip="Github",
            position=NavigationItemPosition.BOTTOM,
        )

        text = self._get_theme_toggle_text()
        self.themeToggleItem = self.navigationInterface.addItem(
            routeKey="theme_toggle",
            icon=FluentIcon.BRIGHTNESS,
            text=text,
            onClick=self.toggle_theme,
            selectable=False,
            tooltip=text,
            position=NavigationItemPosition.BOTTOM,
        )

    def closeEvent(self, e):
        if hasattr(self, "poedit_thread"):
            self.poedit_thread.stop()
        if hasattr(self, "q_thread"):
            self.q_thread.quit()
            self.q_thread.wait(1000)
        if hasattr(self, "translate_thread"):
            self.translate_thread.quit()
            self.translate_thread.wait(1000)
        if hasattr(self, "llm_translate_thread"):
            self.llm_translate_thread.quit()
            self.llm_translate_thread.wait(1000)
        super().closeEvent(e)
