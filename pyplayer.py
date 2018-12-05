import sys
import time
from PyQt5 import QtGui, QtWidgets, QtCore, uic

app = QtWidgets.QApplication([])
window = uic.loadUi("pyplayer.ui")

window.show()
app.exec()
