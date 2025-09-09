from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from controller import Controller
from PyQt5.QtCore import Qt

class AirSimGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Status")

        layout=QVBoxLayout(self)
        self.status=QLabel("Present Button:",self)
        self.image=QLabel(self)
        self.image.setStyleSheet("background-color: lightgray;")
        layout.addWidget(self.status)
        layout.addWidget(self.image)

        self.drone=Controller()
        self.drone.start()
    
    def update_status(self,mode):
        self.status.setText(f"Present Button: {mode}")

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_W:
            self.update_status("forward")
        elif event.key() == Qt.Key_S:
            self.update_status("backward")
        elif event.key() == Qt.Key_A:
            self.update_status("left")
        elif event.key() == Qt.Key_D:
            self.update_status("right")
        elif event.key() == Qt.Key_Space:
            self.update_status("hover")
        elif event.key() == Qt.Key_Shift:
            self.update_status("dropping")
        elif event.key() == Qt.Key_L:
            self.update_status("land")