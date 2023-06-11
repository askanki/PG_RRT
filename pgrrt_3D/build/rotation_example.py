from scipy.spatial.transform import Rotation as R
import numpy as np

#r = R.from_quat([0, 0, np.sin(np.pi/4), np.cos(np.pi/4)])
#
#r.as_matrix()
#array([[ 2.22044605e-16, -1.00000000e+00,  0.00000000e+00],
#[ 1.00000000e+00,  2.22044605e-16,  0.00000000e+00],
#[ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
#r.as_rotvec()
#array([0.        , 0.        , 1.57079633])
#r.as_euler('zyx', degrees=True)
#array([90.,  0.,  0.])

#Global FOR
r = R.from_euler('zyx', [90,0,90], degrees=True)
print("Global ", r.as_dcm())

#Body FOR
r = R.from_euler('ZYX', [90,0,90], degrees=True)
print("Local ", r.as_dcm())