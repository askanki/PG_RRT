import numpy as np
import matplotlib.pyplot as plt
from fancyArroePatch import Arrow3D
from mpl_toolkits.mplot3d import Axes3D

def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(Axes3D, 'arrow3D', _arrow3D)

fig = plt.figure()
ax = plt.axes(projection='3d')
# while(True):
# f_ = open("../H.txt", "r+")
f_ = open("../map", "r+")
line = f_.readline()
x_obs= []
y_obs= []
while line:
    line = list(map(float, line.split(" ")))
    #plt.plot(line[0], line[1], color="black", marker="o")
    x_obs.append(line[0])
    y_obs.append(line[1])
    line = f_.readline()
f_.close()

loop_iter = 0
while True:
#while loop_iter < 10:
    loop_iter += 1 
    plt.cla()
    plt.axis("equal")
    
    plt.plot(x_obs,y_obs, color="black", marker="o",linestyle=" ")
    f = open("../cmake-build-debug/path_raw.txt", "r+")
    line = f.readline()
    k = 0
    start = []
    end = []
    
    while line:
        line = list(map(float, line.split(" ")))
        if k==0:
            start = line
        elif k==1:
            end = line
        else:
        #     ##plt.plot([line[0], line[2]], [line[1], line[3]], color="b", alpha=0.2)
        #     ##plt.arrow(line[2], line[3], line[0]-line[2], line[1]-line[3], shape='full', lw=1, length_includes_head=True, head_width=.05, ec="blue", alpha=0.2)
            ax.arrow3D(line[3], line[4], line[5], line[0]-line[3], line[1]-line[4], line[2]-line[5], lw=1, ec="blue", alpha=0.2)
        #     ax.arrow3D(1,0,0,
        #            1,1,1,
        #            mutation_scale=20,
        #            ec ='green',
        #            fc='red')
        line = f.readline()
        k+=1
    plt.plot(start[0], start[1], color="b", marker="o")
    plt.plot(end[0], end[1], color="r", marker="o")
    

    f = open("../cmake-build-debug/kino.txt", "r+")
    line = f.readline()
    while line:
        line = list(map(float, line.split(" ")))
        ax.arrow3D(line[3], line[4], line[5], line[0]-line[3], line[1]-line[4], line[2]-line[5], lw=1, ec="red", alpha=0.2)
        line = f.readline()
    
    # while True:
    #     f = open("removed.txt", "r+")
    #     line = f.readline()
    #     while line:
    #         line = list(map(float, line.split(" ")))
    #         plt.plot(line[0], line[1], color="red", marker="o")
    #         line = f.readline()
    #     plt.pause(1)
    x =[]
    y =[]
    z = []
    f = open("../cmake-build-debug/path.txt", "r+")
    line = f.readline()
    while line:
        line = list(map(float, line.split(" ")))
        #plt.plot(line[0], line[1], color="green", marker="o")
        x.append(line[0])
        y.append(line[1])
        z.append(line[2])
        line = f.readline()
    ax.plot3D(x, y, z, color="green", marker="o")
    plt.pause(0.5)
    break
    #input()
plt.show()
