# import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import math
# x = [431311, 505589, 641676, 673609, 457581, 411463, 508154, 281950, 211903, 722662, 694179, 531170, 536130, 595067, 404784, 294227, 252800, 18012.1]
# objects = [i for i in range(0,360,20)]
# plt.bar(np.arange(len(objects)), x)
# plt.xticks(np.arange(len(objects)), objects)
# plt.show()
def initial(t1_linear, t1_translation,z1,z2,p):
    # print(t1_linear, z1[0])
    m = np.dot(t1_linear,  z1[0])
    # print(m)
    A = [[0,0]]
    A[0][0] = m[0] - z2[0][0]*m[2]
    A[0][1] = m[1] - z2[0][1]*m[2]

    b = [[0,0]]
    b[0][0] = z2[0][0]*t1_translation[0][2] - t1_translation[0][0]
    b[0][1] = z2[0][1]*t1_translation[0][2] - t1_translation[0][1]
    # print(b, np.dot(A, np.transpose(A)))
    A = np.transpose(A)
    b = np.transpose(b)
    # print("Inverse:", np.linalg.inv(np.dot(np.transpose(A), A)))
    # print(A, "B: ",b)
    inverse = np.linalg.inv(np.dot(np.transpose(A), A))
    depth = np.dot(np.transpose(A), b)
    # print(depth)
    depth = np.dot(inverse, depth)
    print("depth:", depth)

    z1 = np.dot(t1_linear, np.transpose(z1))
    z1 = np.transpose(z1)
    pfc1 = np.multiply(1/math.sqrt(z1[0][0]**2 + z1[0][1]**2 + z1[0][2]**2), z1)
    pfc2 = np.multiply(1/math.sqrt(z2[0][0]**2 + z2[0][1]**2 + z2[0][2]**2), z2)

    pfc1 = np.transpose(pfc1)
    pfc2 = np.transpose(pfc2)
    A = np.concatenate([pfc1, np.multiply(-1, pfc2)], axis=1)
    b = t1_translation
    b = np.transpose(b)
    # print(A)
    inverse = np.linalg.inv(np.dot(np.transpose(A), A))
    # print(inverse, b)
    depth = np.dot(np.transpose(A), b)
    depth = np.dot(inverse, depth)
    point = np.multiply(depth[0][0],pfc1)
    print("")
    print(point)
intrinsic = np.array([[202.250620, 0, 97.851939], [0., 201.533760, 82.647231], [0.,0.,1.]], dtype=np.float32)
d_coeff = np.array([-0.403591, 0.167151, 0.001863, 0.001011, 0.], dtype=np.float32)
# point = np.zeros((10,1,2), dtype=np.float32)
# point1 = cv.undistortPoints(point, intrinsic, d_coeff)
# point2 = cv.undistortPoints([67,76],[[202.250620, 0, 97.851939], [0, 201.533760, 82.647231], [0,0,1]],[-0.403591, 0.167151, 0.001863, 0.001011])
# print(point1)
# intrinsic = np.array([[1.3e+03, 0., 6.0e+02], [0., 1.3e+03, 4.8e+02], [0., 0., 1.]], dtype=np.float32)
# d_coeff = np.array([-2.4e-01, 9.5e-02, -4.0e-04, 8.9e-05, 0.], dtype=np.float32)

theta = 45*math.pi/180
# test = np.zeros((1,1,2), dtype=np.float32)
test = np.array([[[3/4.,0.]]], dtype=np.float32)
test1 = np.array([[[-3/4.,0.]]], dtype=np.float32)
print(test, test1)
xy_undistorted = cv.undistortPoints(test, intrinsic, d_coeff)
xy_undistorted1 = cv.undistortPoints(test1, intrinsic, d_coeff)
xy_undistorted = np.append(xy_undistorted[0][0], [1.])
xy_undistorted1 = np.append(xy_undistorted1[0][0], [1.])
print(xy_undistorted, xy_undistorted1)
# xy_undistorted = [-0.399845362, -0.0354694501, 1.]
# xy_undistorted1 = [-0.401175797, -0.0349662118, 1.]

t1_linear = [[math.cos(theta), 0, math.sin(theta)],
             [0, 1, 0],
             [-math.sin(theta), 0, math.cos(theta)]]

t1_linear = [[0.999984,  0.000144849,  -0.00565534],
            [-0.000211343,     0.999931,   -0.0117587],
            [0.00565324,    0.0117597,     0.999915]]
t1_translation = [[-0.0192839, 0.00447549, -0.0243378]]
# inverse_rot = np.linalg.inv(t1_linear)
# point2 = np.dot(inverse_rot, [3/4., 0., 1.])
# print("Point: ", point2)
# print(t1_linear)
# print(inverse_rot)
print("////////////////")

pointa = [[0.350581, -0.134716, 1.]]
pointb = [[0.344966, -0.146619, 1.]]
# initial(t1_linear, [[6.,0.0,0.0]],[point2],[[-3/4, 0., 1.]], 0.)
initial(t1_linear, t1_translation, pointa, pointb, 0.)
# initial(np.identity(3), [[-6.,0.0,0.0]],[xy_undistorted], [xy_undistorted1], 0.)
