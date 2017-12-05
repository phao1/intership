import sys
from PyQt4.QtGui import *
a = QApplication(sys.argv)
w = QWidget()
w.resize(320, 240)
w.setWindowTitle("Hello, World!")
w.show()
sys.exit(a.exec_())