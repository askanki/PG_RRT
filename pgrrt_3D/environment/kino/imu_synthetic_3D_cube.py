import math
import numpy as np
# file = open("imu_data_sythetic.txt", "w+")
# acc = 0.0
# x_mean = 0.0
# x_variance = 0*7*(10**-4)
# y_mean = 0.0
# y_variance = 0*8*(10**-4)
# z_mean = 0.0
# z_variance = 0*0.00155
# length = 5000
#
#
# for q in range(length - 1):
#     # acc += 0.0004
#     if q == 601:
#         file.write(str("12.0" + " 0.0 0.0" +  "\n"))
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
#

# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(x_mean, x_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(acc) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(x_mean, x_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(-acc) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(z_mean, z_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) +" " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(acc) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(z_mean, z_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(-acc) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(10 + y_mean, y_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(acc) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(10 - y_mean, y_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(acc) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(x_mean, x_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(-acc) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(x_mean, x_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(acc) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(10 - y_mean, y_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(acc) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(10 + y_mean, y_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(acc) + " " + str(np.random.normal(z_mean, z_variance, 1)[0]) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(z_mean, z_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(-acc) + "\n")
# acc = 0.1
# for q in range(length):
#     # acc += 0.0004
#     acc = np.random.normal(z_mean, z_variance, 1)[0]
#     acc = round(acc, 7)
#     file.write(str(np.random.normal(x_mean, x_variance, 1)[0]) + " " + str(np.random.normal(10 + y_mean, y_variance, 1)[0]) + " " + str(acc) + "\n")
# file.close()
## ////////////////////////////////////////////////////// TRAJECTORY GENERATION /////////////////////////////////////////////////////////////////////////////////////////////////
file = open("trajectory.csv","w+")
ts = 0
# pos = 0.
file.write("# timestamp, x, y, z, qx, qy, qz, qw\n")
# for i in range(0, 100*10**6, 10**6):
#     ts+=i
#     file.write(str(ts) + str(", ") + str(pos) +str(", 0., 0., 0., 0., 0., 1.\n"))
#     pos-=4/100
# for i in range(0, 500*10**6, 10**6):
#     ts+=i
#     file.write(str(ts) + str(", ") + str(pos) +str(", 0., 0., 0., 0., 0., 1.\n"))
# ts+=10**6

#///////////////////////////////////////////////////////////////////////// SQUARE TRAJECTORY //////////////////////////////////////////////////////////////////////////////////////////////////////////////
v_x=0.
v_y=0.
v_z=0.
acc=1.

pos_x=-2.0
pos_y=-2.0
pos_z= 0.5
secs = 2 #should be integer
theta = 0.0

qx, qy, qz, qw = 0., 0., 0., 1.

def euler_to_quaternion(yaw, pitch, roll):
    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

    return [qx, qy, qz, qw]

qx, qy, qz, qw = euler_to_quaternion(0*math.pi/180, 0*math.pi/180, 0*math.pi/180)
#qx, qy, qz, qw = euler_to_quaternion(0*math.pi/180, 0*math.pi/180, -90*math.pi/180)

for i in range(0, secs*100*10**7, 10**7):
    ts=i
    file.write(
        str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", ") + str(qx) + str(", ") + str(qy)+ str(", ") + str(qz)+ str(", ") + str(qw) + str("\n"))
    pos_x+=v_x*10**-2+.5*acc*10**-4
    v_x+=acc*10**-2

for i in range(ts+0, ts+secs*100*10**7, 10**7):
    ts = i
    file.write(
        str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", ") + str(qx) + str(", ") + str(qy)+ str(", ") + str(qz)+ str(", ") + str(qw) + str("\n"))
    pos_y += v_y * 10 ** -2 + .5 * acc * 10 ** -4
    v_y += acc * 10**-2


for i in range(ts+0, ts+secs*100*10**7, 10**7):
    ts = i
    file.write(
        str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
    pos_z += v_z * 10 ** -2 + .5 * acc * 10 ** -4
    v_z += acc * 10**-2

v_x = 0.
v_y = 0.
v_z = 0.

for i in range(ts+0, ts+secs*100*10**7, 10**7):
    ts = i
    file.write(
        str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
    pos_x += v_x * 10 ** -2 + .5 * -acc * 10 ** -4
    v_x += -acc * 10 ** -2

for i in range(ts+0, ts+secs*100*10**7, 10**7):
    ts = i
    file.write(
        str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
    pos_y += v_y * 10 ** -2 + .5 * -acc * 10 ** -4
    v_y += -acc * 10 ** -2


for i in range(ts+0, ts+secs*100*10**7, 10**7):
    ts = i
    file.write(
        str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
    pos_z += v_z * 10 ** -2 + .5 * -acc * 10 ** -4
    v_z += -acc * 10 ** -2

file.close()