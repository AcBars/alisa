import sys

from PyQt6.QtWidgets import QApplication

# import db_app
import gui

# db_app.create_db()

app = QApplication(sys.argv)

window = gui.MainWindow()
window.show()

app.exec()

# db_app.read('students')
# db_app.read('classes')
# db_app.read('subjects')
