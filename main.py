from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    from app.views.main_window import MainWindow

    w = MainWindow()
    w.show()
    app.exec()
