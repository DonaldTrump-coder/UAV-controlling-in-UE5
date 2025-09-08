from ui.GUI import AirSimGUI
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
gui=AirSimGUI()
gui.show()
sys.exit(app.exec_())