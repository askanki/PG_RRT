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
dts = 10**7
start_pos = -2.
acc = 0.5
dpos = 0.

file.write("# timestamp, x, y, z, qx, qy, qz, qw\n")
# for i in range(0, 100*10**6, 10**6):
#     ts+=i
#     file.write(str(ts) + str(", ") + str(pos) +str(", 0., 0., 0., 0., 0., 1.\n"))
#     pos-=4/100
# for i in range(0, 500*10**6, 10**6):
#     ts+=i
#     file.write(str(ts) + str(", ") + str(pos) +str(", 0., 0., 0., 0., 0., 1.\n"))
# ts+=10**6
#### Ankit edited######

for i in range(0, 400):
    ts += dts
    pos = start_pos + dpos
    file.write(str(ts) + str(", ") + str(pos) +str(", 0., 0., 0., 0., 0., 1.\n"))
    dpos = 0.5 * acc * ts * ts * 10**-18
# for i in range(0, 500*10**6, 10**6):
#     ts+=i
#     file.write(str(ts) + str(", ") + str(pos) +str(", 0., 0., 0., 0., 0., 1.\n"))
#ts+=10**6

#///////////////////////////////////////////////////////////////////////// SQUARE TRAJECTORY //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# v_x=0.
# v_y=0.
# acc=1.
# pos_x=-4.
# pos_y=-4.
# pos_z= 0.
# secs = 2 #should be integer
# for i in range(0, secs*100*10**7, 10**7):
#     ts=i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_x+=v_x*10**-2+.5*acc*10**-4
#     v_x+=acc*10**-2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts = i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_x += v_x * 10 ** -2 + .5 * -acc * 10 ** -4
#     v_x += -acc * 10 ** -2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts = i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_y += v_y * 10 ** -2 + .5 * acc * 10 ** -4
#     v_y += acc * 10 ** -2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts = i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_y += v_y * 10 ** -2 + .5 * -acc * 10 ** -4
#     v_y += -acc * 10 ** -2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts=i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_x+=v_x*10**-2+.5*-acc*10**-4
#     v_x+=-acc*10**-2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts = i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_x += v_x * 10 ** -2 + .5 * acc * 10 ** -4
#     v_x += acc * 10 ** -2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts = i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_y += v_y * 10 ** -2 + .5 * -acc * 10 ** -4
#     v_y += -acc * 10 ** -2
# for i in range(ts+0, ts+secs*100*10**7, 10**7):
#     ts = i
#     file.write(
#         str(i) + str(", ") + str(pos_x) + str(", ") + str(pos_y) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#     pos_y += v_y * 10 ** -2 + .5 * acc * 10 ** -4
#     v_y += acc * 10 ** -2

########Circular Code#########################
# r=-2.0
# pos_z = 2.0
# pos_x_init = 0.0
# ts = 0.0
# resolution = 10
# theta_check = []
# for theta1 in range(0,360):
#     for theta in range(resolution):
#         theta = theta1 + theta/resolution
#         theta = theta*math.pi/180
#         if theta in theta_check:
#             print("error")
#         theta_check.append(theta)
#         file.write(str(ts) + str(", ") + str(r*math.cos(theta) + pos_x_init) + str(", ") + str(r*math.sin(theta)) + str(", ") + str(pos_z) + str(", 0., 0., 0., 1.\n"))
#         # file.write(str(i) + str(", ") + str(r*math.cos(theta)) + str(", ") + str(r*math.sin(theta)) + str(", ") + str(pos_z) + str(", 0.5, 0.5, 0.5, 0.5\n"))
#         ts += 10**7
# print(theta_check)
file.close()