import matplotlib.pyplot as plt

plt.axis("equal")
# while(True):
# f_ = open("../H.txt", "r+")
f_ = open("../map", "r+")
line = f_.readline()
while line:
    line = list(map(float, line.split(" ")))
    plt.plot(line[0], line[1], color="black", marker="o")
    line = f_.readline()
f_.close()
# plt.pause(1)
#
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
        #plt.plot([line[0], line[2]], [line[1], line[3]], color="b", alpha=0.2)
        #plt.arrow(line[2], line[3], line[0]-line[2], line[1]-line[3], shape='full', lw=1, length_includes_head=True, head_width=.05, ec="blue", alpha=0.2)
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
while True:
    f = open("path.txt", "r+")
    line = f.readline()
    while line:
        line = list(map(float, line.split(" ")))
        plt.plot(line[0], line[1], color="green", marker="o")
        line = f.readline()
    plt.pause(0.5)
plt.show()
