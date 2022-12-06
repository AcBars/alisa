import sys

from PyQt6.QtWidgets import QApplication

import db_app
import gui

db_app.create_db()

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()

app.exec()
