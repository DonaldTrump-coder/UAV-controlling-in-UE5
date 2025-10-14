import pyqtgraph.opengl as gl
import numpy as np

class PointCloudWidget(gl.GLViewWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # 相机与坐标轴
        self.setCameraPosition(distance=10)
        self.opts['center'] = (0, 0, 0)
        self.showGrid(x=True, y=True, z=True)

        # 初始化点云数据
        self.points = np.zeros((0, 3))
        self.colors = np.ones((0, 4))

        self.scatter = gl.GLScatterPlotItem(pos=self.points, color=self.colors, size=5)
        self.addItem(self.scatter)