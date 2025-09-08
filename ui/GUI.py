from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel
from controller import Controller

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