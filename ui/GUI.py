from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel,QHBoxLayout
from controller import Controller
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage,QPixmap
from pynput import keyboard

class AirSimGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone Status")

        layout=QVBoxLayout(self)
        self.status=QLabel("Present Button: None",self)
        hbox = QHBoxLayout(self)
        self.image=QLabel(self)
        self.image.setStyleSheet("background-color: lightgray;")
        self.coordinate=QLabel(self)
        hbox.addWidget(self.image)
        hbox.addWidget(self.coordinate)
        layout.addWidget(self.status)
        layout.addLayout(hbox)

        self.drone=Controller()
        self.drone.image_signal.connect(self.update_image)
        self.drone.coordinage_signal.connect(self.update_coordinates)
        self.drone.start()
        
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
    
    def update_status(self,mode):
        self.status.setText(f"Present Button: {mode}")

    def update_image(self,qimg:QImage):
        pixmap = QPixmap.fromImage(qimg)
        self.image.setPixmap(pixmap)

    def update_coordinates(self,coordinate:list):
        #update the coordinates of drone
        self.coordinate.setText(f"X:{coordinate[0]} Y:{coordinate[1]} Z:{coordinate[2]}")
        
    def on_press(self, key):
        try:
            if key.char == 'w':
                self.update_status("W")
                self.drone.set_status("Forward")
            elif key.char == 's':
                self.update_status("S")
                self.drone.set_status("Backward")
            elif key.char == 'a':
                self.update_status("A")
                self.drone.set_status("Left")
            elif key.char == 'd':
                self.update_status("D")
                self.drone.set_status("Right")
            elif key.char == 'q':
                self.update_status("Q")
                self.drone.set_status("Turn Left")
            elif key.char == 'e':
                self.update_status("E")
                self.drone.set_status("Turn Right")
            elif key.char == 'p':
                self.update_status("P")
                self.drone.set_status("Take Image")
        except AttributeError:
            # 处理特殊按键
            if key == keyboard.Key.space:
                self.update_status("Space")
                self.drone.set_status("Hover")
            elif key == keyboard.Key.shift:
                self.update_status("Shift")
                self.drone.set_status("Dropping")
            elif key == keyboard.Key.l:
                self.update_status("L")
                self.drone.landing()
            elif key == keyboard.Key.h:
                self.update_status("H")
                self.drone.takeoff()

    def on_release(self, key):
        # 松开按键时恢复为 None
        self.update_status("None")
        self.drone.set_status("None")

    def closeEvent(self, event):
        self.listener.stop()
        self.drone.landing()
        self.drone.running=False
        self.drone.wait()
        event.accept()