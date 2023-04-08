import csv
import matplotlib.pyplot as plt
file = open("IMU_readings.txt", "r")
file1 = open("IMU_readings.csv", "w+")
fig, axs = plt.subplots(3,4)

csv_reader = csv.reader(file)
pos_z = 0.0
pos_x = 0.0
pos_y = 0.0
u_z = 0.0
u_y = 0.0   #-0.3490658503988659
u_x = 0.0

max_ux = 0.0
line = file.readline()
ts = float(line.split(',')[0])
ts0 = float(line.split(',')[0])
sum_accel = 0.
count = 0
while(line):
    # print(line.split(','))
    rows = line.split(',')
    count +=1
    # print(rows)
    # print(rows[31]," poz: " ,pos_z, " u: ", u_z, " delv: ", float(rows[31])*10**-3)
    del_t = (float(rows[0]) - ts)*10**-9
    # print(del_t)
    ts  = float(rows[0])
    accel = float(rows[29]) ##- 9.81 float(rows[29]) ##- 9.81
    accel1 = float(rows[30]) ##- 9.81 float(rows[30]) ##- 9.81
    accel2 = float(rows[31]) - 9.81 #float(rows[31]) ##- 9.81
    if count%1000==0:
        axs[0, 0].plot(ts, accel, marker="o", color="red")
        axs[1, 0].plot(ts, u_x, marker="o", color="red")
        axs[2, 0].plot(ts, pos_x, marker="o", color="red")
        axs[0, 1].plot(ts, accel1, marker="o", color="green")
        axs[1, 1].plot(ts, u_y, marker="o", color="green")
        axs[2, 1].plot(ts, pos_y, marker="o", color="green")
        axs[0, 2].plot(ts, accel2, marker="o", color="orange")
        axs[1, 2].plot(ts, u_z, marker="o", color="orange")
        axs[2, 2].plot(ts, pos_z, marker="o", color="orange")
        axs[0, 3].plot(ts, (accel**2 + accel1**2)**0.5, marker=".", color="blue")
        axs[1, 3].plot(ts, (u_x**2 + u_y**2)**0.5,  marker=".", color="blue")
        axs[2, 3].plot(ts, (pos_x**2 + pos_y**2)**0.5, marker=".", color="blue")
        plt.pause(0.01)
    sum_accel+=accel
    pos_x += u_x * del_t + 0.5 * accel  * del_t ** 2
    pos_y += u_y * del_t + 0.5 * accel1 * del_t ** 2
    pos_z += u_z * del_t + 0.5 * accel2 * del_t ** 2
    u_x += accel*del_t
    u_y += accel1*del_t
    u_z += accel2*del_t
    if max_ux < u_x:
        max_ux = u_x
    file1.write(str(pos_x) + str(" ") + str(pos_y) + str(" ")+ str(pos_z) + "\n")
    # pos_z_ += u_z*del_t
    line = file.readline()
print((ts-ts0)*10**-9)
print(pos_x, pos_y, pos_z, "MAx velocity in x: ", max_ux)
plt.show()
file.close()
file1.close()