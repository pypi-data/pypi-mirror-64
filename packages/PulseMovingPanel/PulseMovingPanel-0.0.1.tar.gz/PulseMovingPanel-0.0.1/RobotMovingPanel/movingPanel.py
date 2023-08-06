import sys
import config

from PyQt5.QtWidgets import QApplication
from interface.interfaceLogic import MovingPanel

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MovingPanel()
    window.show()
    app.exec_()