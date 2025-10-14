import numpy as np

X = 0
Y = 0
Z = 0
Pitch = 0
Yaw = 0
Roll = 0 # degrees

def inverse_UE_transform(x_world, y_world, z_world):
    # rotations and translation in of GS in UE
    pitch, yaw, roll = np.radians([Pitch, Yaw, Roll])

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]
    ])
    
    Ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    
    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0, 0, 1]
    ])

    R = Rz @ Ry @ Rx
    T = np.array([X, Y, Z])
    P_world = np.array([x_world, y_world, z_world])
    P_local = R.T @ (P_world - T)
    return float(P_local[0]), float(-P_local[1]), float(P_local[2]) # left-handed to right-handed