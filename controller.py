import airsim
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

class Controller(QThread):

    image_signal=pyqtSignal(QImage) #signal to send image

    def __init__(self):
        super().__init__()
        client = airsim.MultirotorClient()
        client.confirmConnection()
        client.enableApiControl(True)
        client.armDisarm(True)
        client.takeoffAsync().join() #taking off before controlling