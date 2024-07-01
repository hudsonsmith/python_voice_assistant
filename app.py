import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QIcon, QPixmap

APOLLO_App = QApplication([])

window = QMainWindow()
window.setMinimumSize(600,400)
window.setWindowTitle("APOLLO - A dAIlight Technologies application")
window.setWindowIcon(QIcon("Screenshot 2024-06-30 190100.png"))

APOLLO_Button = QLabel()
APOLLO_Button.setPixmap(QPixmap())

window.show()
APOLLO_App.exec()
