import pyqtgraph.opengl as gl
import numpy as np
from PyQt5.QtGui import QVector3D

class PointCloudWidget(gl.GLViewWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        # 相机与坐标轴
        self.setCameraPosition(distance=10)
        self.opts['center'] = QVector3D(0, 0, 0)
        
        # 添加网格
        grid_x = gl.GLGridItem()
        grid_y = gl.GLGridItem()
        grid_z = gl.GLGridItem()

        # 旋转以让网格分别在 XY、YZ、XZ 平面上
        grid_x.rotate(90, 0, 1, 0)
        grid_y.rotate(90, 1, 0, 0)
        grid_x.translate(-5, 0, 0)
        grid_y.translate(0, -5, 0)
        grid_z.translate(0, 0, -5)

        self.addItem(grid_x)
        self.addItem(grid_y)
        self.addItem(grid_z)

        # 初始化点云数据
        self.points = np.zeros((0, 3))
        self.colors = np.ones((0, 4))

        self.scatter = gl.GLScatterPlotItem(pos=self.points, color=self.colors, size=5)
        self.addItem(self.scatter)

    def update_pointcloud(self, points: np.ndarray):
        if points is None or len(points) == 0:
            return
        self.points = np.asarray(points, dtype=float)
        self.colors = np.ones((len(points), 4))
        self.scatter.setData(pos=self.points, color=self.colors)