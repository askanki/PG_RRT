import tkinter
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


fig = plt.axes(projection="3d")
def line_3d(point1, point2):
    fig.plot3D([point1[0], point2[0]], [point1[1], point2[1]], [point1[2], point2[2]], color="grey", marker="o")

def point_3d(point):
    fig.scatter3D(point[0], point[1], point[2], color="red", marker="o")
