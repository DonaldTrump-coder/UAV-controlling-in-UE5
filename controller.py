import airsim
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import numpy as np
import cv2
import time

class Controller(QThread):

    image_signal=pyqtSignal(QImage) #signal to send image
    coordinage_signal = pyqtSignal(list)
    status="None"

    def __init__(self):
        super().__init__()
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join() #taking off before controlling
        self.running=True
        self.landed=False

    def takeoff(self):
        self.client.takeoffAsync().join()
        self.landed=False

    def landing(self):
        self.client.landAsync().join()
        self.landed=True

    def set_status(self,status:str):
        self.status=status

    def forward(self):
        self.client.moveByVelocityBodyFrameAsync(vx=2, vy=0, vz=0, duration=0.1).join()
    
    def backward(self):
        self.client.moveByVelocityBodyFrameAsync(vx=-2, vy=0, vz=0, duration=0.1).join()

    def move_left(self):
        self.client.moveByVelocityBodyFrameAsync(vx=0, vy=-2, vz=0, duration=0.1).join()

    def move_right(self):
        self.client.moveByVelocityBodyFrameAsync(vx=0, vy=2, vz=0, duration=0.1).join()

    def hover(self):
        self.client.moveByVelocityBodyFrameAsync(vx=0, vy=0, vz=-2, duration=0.1).join()

    def drop(self):
        self.client.moveByVelocityBodyFrameAsync(vx=0, vy=0, vz=2, duration=0.1).join()

    def turn_left(self):
        self.client.rotateByYawRateAsync(yaw_rate=-5, duration=0.1).join()

    def turn_right(self):
        self.client.rotateByYawRateAsync(yaw_rate=5, duration=0.1).join()

    def get_coordinate(self):
        # get UE coordinate of Drone
        state = self.client.getMultirotorState()
        pos = state[0].kinematics_estimated.position
        x_ned, y_ned, z_ned = pos.x_val, pos.y_val, pos.z_val
        self.x_ue = y_ned * 100
        self.y_ue = x_ned * 100
        self.z_ue = -z_ned * 100

    def take_image(self):
        png_image = self.client.simGetImage("0", airsim.ImageType.Scene)
        np_img = np.frombuffer(png_image, dtype=np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # BGR -> RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        # OpenCV → QImage
        qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_signal.emit(qimg)

    def run(self):
        while self.running is True:
            self.get_coordinate()
            self.coordinage_signal([self.x_ue,self.y_ue,self.z_ue])
            if self.landed is True:
                continue
            if self.status == "None":
                continue
            elif self.status == "Forward":
                self.forward()
            elif self.status == "Backward":
                self.backward()
            elif self.status == "Left":
                self.move_left()
            elif self.status == "Right":
                self.move_right()
            elif self.status == "Hover":
                self.hover()
            elif self.status == "Dropping":
                self.drop()
            elif self.status == "Turn Left":
                self.turn_left()
            elif self.status == "Turn Right":
                self.turn_right()