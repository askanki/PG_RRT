import matplotlib.pyplot as plt
from shapely.geometry import Polygon

obstacles = []
points_map = {}
points = []
def plot_point(points):
#     #print(point)
    for point in points:
        plt.plot(point[0], point[1], color='red', marker='.')


def add_obstacle(poly):
    obstacles.append(poly)


def point_to_poly(point, offset=0.125):

    x1, y1 = point[0] - offset, point[1] + offset
    x3, y3 = point[0] + offset, point[1] - offset
    x2, y2 = point[0] + offset, point[1] + offset
    x4, y4 = point[0] - offset, point[1] - offset
    return Polygon([(x1,y1), (x2,y2), (x3,y3), (x4,y4)])


def node_to_poly(point):
    x1, y1 = point[0] - 0.065, point[1] + 0.065
    x3, y3 = point[0] + 0.065, point[1] - 0.065
    x2, y2 = point[0] + 0.065, point[1] + 0.065
    x4, y4 = point[0] - 0.065, point[1] - 0.065
    return Polygon([(x1,y1), (x2,y2), (x3,y3), (x4,y4)])


def get_obstacles():
    return obstacles


def get_obs_map():
    return points_map

def get_points():
    return points


with open("maps/H.txt") as file:
    line = file.readline()
    while line:
        line = list(map(float, line.split(" ")))
        obs = point_to_poly((line[0], line[1]))
        obstacles.append(obs)
        # obs1 = point_to_poly((-line[0], line[1]))
        # obstacles.append(obs1)
        # obstacles.append(point_to_poly((-line[0], line[1])))
        points_map[(line[0], line[1])] = obs
        # points_map[(-line[0], line[1])] = obs1
        points.append((line[0], line[1]))
        # points.append((-line[0], line[1]))
        #plt.pause(0.01)
        line = file.readline()
    points.sort(key=lambda x: (x[0], x[1]))
# for x,y in points:
#     print(x, y)
# plot_point(points)
# plt.show()

# 3,9    10,15
# 12,4   15,10
# 4.8,4.5
# 15.2, 15.2