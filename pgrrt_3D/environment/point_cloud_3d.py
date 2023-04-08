import matplotlib.pyplot as plt
import numpy
from shapely.geometry import Polygon, Point

obstacles = []
points_map = {}
points = []
def plot_point(points):
    for point in points:
        plt.plot(point[0], point[1], color='red', marker='.')


def add_obstacle(poly):
    obstacles.append(poly)


def get_obstacles():
    return obstacles


def get_points():
    return points


def get_obs_map():
    return obstacles

with open("map1.txt") as file:
    line = file.readline()
    while line:
        line = list(map(float, line.split(" ")))
        if len(line) == 2:
            line.append(0.)
        points.append((line[0], line[1], line[2]))
        line = file.readline()
    points.sort(key=lambda x: (x[0], x[1]))
    obstacles = numpy.asarray(points)
