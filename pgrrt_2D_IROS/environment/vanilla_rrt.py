import copy
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import random
from shapely.geometry import LineString, Point, Polygon

import tkinter #matplotlib dependency

"""///////////////////////////////////"""
from map_canvas import Canvas
import point_cloud

class Tree:
    def __init__(self, canvas, step_size=0.5):
        self.nodes = []
        self.parent = {}
        self.canvas = canvas
        self.step_size = step_size
        self.nodes.append(canvas.start)
        self.parent[canvas.start] = canvas.start

    def make_action(self, parent, node):
        sample = extend(parent, node, self.step_size)
        return sample

    def add_node(self, parent, node):
        collision_free = True
        if not self.canvas.adv_check_collision(node, parent, self.step_size):  # True if no obstacles
            self.nodes.append(node)
            self.parent[node] = parent
            plt.plot([parent[0], node[0]], [parent[1], node[1]], color="blue")
        else:
            collision_free = False
        return True if collision_free else False


def extend(node1, goal, growth):
    distance = math.sqrt((node1[0] - goal[0]) ** 2 + (node1[1] - goal[1]) ** 2)
    ratio = growth / distance
    return ((1 - ratio) * node1[0] + ratio * goal[0]), ((1 - ratio) * node1[1] + ratio * goal[1])


def eul_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def pick_random(tree, bias=0.4):
    random_index = random.randint(0, len(tree.nodes) - 1)
    parent = tree.nodes[random_index]
    is_bias = random.random()
    if is_bias > bias:
        x_min, x_max, y_min, y_max = -20, 40, -20, 20
        x, y = random.uniform(x_min, x_max), random.uniform(y_min, y_max)
    else:
        x, y = tree.canvas.end
    new_node = tree.make_action(parent, (x,y))
    return parent, new_node


def termination(tree1, tree2, new_node):
    if eul_dist((tree1.canvas.end), new_node) < 0.1:
        return True

    for x in range(len(tree2.nodes)):
        if eul_dist(new_node, tree2.nodes[x]) < 0.5 * tree1.step_size:
            return True
    return False


def build_rrt():
    canvas = Canvas(Polygon([(-5, -20), (40, -20), (40, 20), (-5, 20)]), (1, -5), (13, -5))
    canvas1 = Canvas(Polygon([(-5, -20), (40, -20), (40, 20), (-5, 20)]), (13, -5), (1, -5))

    # canvas = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (10, 15), (35, 17))
    # canvas1 = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (35, 17), (10, 15))
    obstacles = point_cloud.get_obstacles()
    canvas.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    canvas1.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    tree = Tree(canvas)
    tree1 = Tree(canvas1)
    iterations = 0
    for obs in tree.canvas.obstacles:
        plt.plot(*obs.exterior.xy)
    plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')
    plt.pause(0.1)
    while True:
        parent, new_node = pick_random(tree)
        parent1, new_node1 = pick_random(tree1)
        change = tree.add_node(parent, new_node)
        change1 = tree1.add_node(parent1, new_node1)
        if change:
            if termination(tree, tree1, new_node):
                return tree, tree1, iterations
        if change1:
            if termination(tree1, tree, new_node1):
                return tree, tree1, iterations
        iterations += 2
        if iterations % 1000 == 0:
            plt.pause(0.01)
            print(iterations, datetime.datetime.now())

    return tree, tree1, iterations


if __name__ == "__main__":
    print("Start time-stamp: ", datetime.datetime.now())
    tree, tree1, iterations = build_rrt()
    print("End time-stamp: ", datetime.datetime.now())
    print("Iterations: ", iterations)
    print("Nodes: ", len(tree.nodes) + len(tree1.nodes))