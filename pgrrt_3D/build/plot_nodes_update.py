import matplotlib.pyplot as plt

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
    f = open("path_raw.txt", "r+")
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
            ##plt.plot([line[0], line[2]], [line[1], line[3]], color="b", alpha=0.2)
            ##plt.arrow(line[2], line[3], line[0]-line[2], line[1]-line[3], shape='full', lw=1, length_includes_head=True, head_width=.05, ec="blue", alpha=0.2)
            plt.arrow(line[3], line[4], line[0]-line[3], line[1]-line[4], shape='full', lw=1, length_includes_head=True, head_width=.05, ec="blue", alpha=0.2)
        line = f.readline()
        k+=1
    plt.plot(start[0], start[1], color="b", marker="o")
    plt.plot(end[0], end[1], color="r", marker="o")
    

    f = open("kino.txt", "r+")
    line = f.readline()
    while line:
        line = list(map(float, line.split(" ")))
        plt.arrow(line[2], line[3], line[0]-line[2], line[1]-line[3], shape='full', lw=1, length_includes_head=True, head_width=.05, ec="red", alpha=0.2)
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
   
    f = open("path.txt", "r+")
    line = f.readline()
    while line:
        line = list(map(float, line.split(" ")))
        #plt.plot(line[0], line[1], color="green", marker="o")
        x.append(line[0])
        y.append(line[1])
        line = f.readline()
    plt.plot(x, y, color="green", marker="o")
    plt.pause(0.5)
    #input()
plt.show()
