from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from controller import Controller
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage,QPixmap

class AirSimGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Status")

        layout=QVBoxLayout(self)
        self.status=QLabel("Present Button: None",self)
        self.image=QLabel(self)
        self.image.setStyleSheet("background-color: lightgray;")
        layout.addWidget(self.status)
        layout.addWidget(self.image)

        self.drone=Controller()
        self.drone.image_signal.connect(self.update_image)
        self.drone.start()
    
    def update_status(self,mode):
        self.status.setText(f"Present Button: {mode}")

    def update_image(self,qimg:QImage):
        pixmap = QPixmap.fromImage(qimg)
        self.image.setPixmap(pixmap)

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_W:
            self.update_status("W")
            self.drone.set_status("Forward")
        elif event.key() == Qt.Key_S:
            self.update_status("S")
            self.drone.set_status("Backward")
        elif event.key() == Qt.Key_A:
            self.update_status("A")
            self.drone.set_status("Left")
        elif event.key() == Qt.Key_D:
            self.update_status("D")
            self.drone.set_status("Right")
        elif event.key() == Qt.Key_Space:
            self.update_status("Space")
            self.drone.set_status("Hover")
        elif event.key() == Qt.Key_Shift:
            self.update_status("Shift")
            self.drone.set_status("Dropping")
        elif event.key() == Qt.Key_L:
            self.update_status("L")
            self.drone.landing()
        elif event.key() == Qt.Key_H:
            self.update_status("H")
            self.drone.takeoff()
        elif event.key() == Qt.Q:
            self.update_status("Q")
            self.drone.set_status("Turn Left")
        elif event.key() == Qt.E:
            self.update_status("E")
            self.drone.set_status("Turn Right")
        elif event.key() == Qt.P:
            self.update_status("P")

    def keyReleaseEvent(self, event):
        self.update_status("None")

    def closeEvent(self, event):
        self.drone.landing()
        self.drone.running=False
        self.drone.wait()
        event.accept()