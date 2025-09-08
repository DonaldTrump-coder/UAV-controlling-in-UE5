import airsim
from PyQt5.QtCore import QThread

class Controller(QThread):
    def __init__(self):
        super().__init__()