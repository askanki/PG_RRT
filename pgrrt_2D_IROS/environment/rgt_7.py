import copy
import cppyy
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import random
from shapely.geometry import LineString, Point, Polygon

import tkinter  # matplotlib dependency

"""///////////////////////////////////"""
from map_canvas import Canvas
import point_cloud
from probability_dist import GMM, Gaussian
from quadtree_2 import Point, Node, Quad

plt.axis("equal")

class Tree:
    def __init__(self, canvas, threshold_theta=90, resolution_angle=90, step_size=0.1):
        self.nodes = []  # List of nodes in the Tree
        self.prob_dist = {}  # Dictionary of nodes -> probability distribution or GMM Model
        self.parent = {}  # Dictionary node -> parent of node
        self.actions = {}  # Dictionary node -> action space
        self.actions_taken = {}  # Dictionary action -> bool, global dictionary of actions, value is True if action is reserved by some node
        """////////////////////////"""
        self.canvas = canvas  # canvas contains start, end position and obstacles
        self.threshold_theta = threshold_theta  # parameter to sensitivity for special node
        self.resolution_angle = resolution_angle  # parameter to set resolution for actions
        self.step_size = step_size  # parameter to set step-size between two consecutive nodes
        """////////////////////////"""
        self.nodes.append(canvas.start)
        self.prob_dist[canvas.start] = GMM([Gaussian(5, 10, 0.5), Gaussian(-5 % 360, 10, 0.5)])
        self.parent[canvas.start] = canvas.start
        self.quadtree = Quad(Point(-25, -25), Point(25, 25), 0.5)
        """////////////////////////"""
        self.setup_action(canvas.start, self.resolution_angle)
        self.actions_taken[canvas.start] = True

    def setup_action(self, node, resolution_angle):
        action = []
        for angle in range(0, 360, resolution_angle):
            sample = extend(node, self.canvas.end, self.step_size)
            sample_location = rotate(node, sample, angle)
            flag = 0
            if self.quadtree.search(Point(sample_location[0], sample_location[1]), 0.075, []):
                flag = 1
            if flag == 0:
                self.actions_taken[sample_location] = True
                action.append((angle, sample_location))
                self.quadtree.insert(Node(Point(sample_location[0], sample_location[1]), (sample_location[0], sample_location[1])))
        if len(action) > 0:
            self.actions[node] = action

    def add_node(self, parent, node, gauss):
        collision_free = True
        if not self.canvas.adv_check_collision(node, parent, self.step_size):  # True if no obstacles
            self.nodes.append(node)
            self.parent[node] = parent
            self.setup_action(node, self.resolution_angle)
        else:
            collision_free = False

        self.change_probability(gauss, collision_free)  # alter the distribution of gaussian based on collision

        if collision_free:
            self.prob_dist[node] = copy.deepcopy(self.prob_dist[parent])  # copy the gaussian of parent
            for gauss_ in self.prob_dist[node].gauss_list:  # modify gaussian of node with bias towards goal
                mean_shift = self.resolution_angle * 0.9
                variance_shift = 2
                gauss_.mean = shift_toward(gauss_.mean, 0, mean_shift)
                gauss_.variance -= variance_shift
                gauss_.variance = max(5, gauss_.variance)

        return True if collision_free else False

    def change_probability(self, gauss, collision_free):
        if collision_free:
            mean_shift = self.resolution_angle * 0.9
            gauss.mean = shift_away(gauss.mean, 0, mean_shift)
            variance_shift = 2
            gauss.variance -= variance_shift
            gauss.variance = max(5, gauss.variance)

        else:
            mean_shift = self.resolution_angle * 0.9
            gauss.mean = shift_away(gauss.mean, 0, mean_shift)
            variance_shift = 4
            gauss.variance += variance_shift
            gauss.variance = max(5, gauss.variance)

    def check_threshold(self, node, parent):
        if min(get_angle(node, parent, self.parent[parent]),
               abs(360 - get_angle(node, parent, self.parent[parent]))) > 180 - self.threshold_theta:
            return True
        return False

    def make_action(self, node, sampled_direction):
        if node in self.actions:
            actions = self.actions[node]
            if len(actions) < 1:
                self.actions.pop(node)
                return False
            closest = actions[0]
            for action in actions:
                if dist_mean(action[0], sampled_direction) < dist_mean(closest[0],
                                                                       sampled_direction):  # replace with dist function
                    closest = action
            self.remove_action(node, closest)
            return closest[1]
        return False

    def remove_action(self, node, action):
        actions = self.actions[node]
        if action in actions:
            self.actions[node].pop(self.actions[node].index(action))
        if len(actions) == 0:
            self.actions.pop(node)


def eul_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def extend(node1, goal, growth):
    distance = math.sqrt((node1[0] - goal[0]) ** 2 + (node1[1] - goal[1]) ** 2)
    ratio = growth / distance
    return ((1 - ratio) * node1[0] + ratio * goal[0]), ((1 - ratio) * node1[1] + ratio * goal[1])


def rotate(origin, point, angle):
    angle *= math.pi / 180
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def shift_toward(mean, centre, shift):
    if abs(dist_mean((mean - shift), centre)) <= abs(dist_mean((mean + shift), centre)):
        mean -= shift
    else:
        mean += shift
    return mean % 360


def shift_away(mean, centre, shift):
    if abs(dist_mean((mean - shift), centre)) <= abs(dist_mean((mean + shift), centre)):
        mean += shift
    else:
        mean -= shift
    return mean % 360


def dist_mean(mean1, mean2):
    return min(abs(mean1 - mean2) % 360, 360 - abs(mean1 - mean2) % 360)


def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def pick_random(tree, iterations):
    while True:
        iterations += 1
        random_index = random.randint(0, len(tree.nodes) - 1)
        parent = tree.nodes[random_index]
        sample_direction, gauss = tree.prob_dist[parent].sample()
        new_node = tree.make_action(parent, sample_direction)
        if new_node:
            return parent, new_node, gauss, iterations


def termination(tree1, tree2, new_node):
    if eul_dist((tree1.canvas.end), new_node) < 0.1:
        return True

    if tree2.quadtree.search(Point(new_node[0], new_node[1]), 0.2, []):
        return True
    return False


def build_rrt():
    canvas = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (-13, -5), (13, -5))
    canvas1 = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (13, -5), (-13, -5))
    obstacles = point_cloud.get_obstacles()
    canvas.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    canvas1.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    tree = Tree(canvas)
    tree1 = Tree(canvas1)
    iterations = 0
    while True:
        parent, new_node, gauss, iterations = pick_random(tree, iterations)
        parent1, new_node1, gauss1, iterations = pick_random(tree1, iterations)
        change = tree.add_node(parent, new_node, gauss)
        change1 = tree1.add_node(parent1, new_node1, gauss1)
        if change:
            if termination(tree, tree1, new_node):
                return tree, tree1, iterations
        if change1:
            if termination(tree1, tree, new_node1):
                return tree, tree1, iterations
        if iterations % 1000 == 0:
            # plt.pause(0.01)
            print(iterations, datetime.datetime.now())
    return tree, tree1, iterations


if __name__ == "__main__":
    print("Start time-stamp: ", datetime.datetime.now())
    tree, tree1, iterations = build_rrt()
    print("End time-stamp: ", datetime.datetime.now())
    print("Iterations: ", iterations)
    print("Nodes: ", len(tree.nodes) + len(tree1.nodes))
    # print(CHECKSUM2)
    # """ Uncomment these to see plot
    obstacles = point_cloud.get_points()
    for obs in obstacles:
        plt.scatter(obs[0], obs[1], marker="s", color="black", s=5)
    plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')

    for nodes in tree.nodes:
        plt.scatter(nodes[0], nodes[1], color="blue", marker="o", alpha=.5, s=5)
    for nodes in tree1.nodes:
        plt.scatter(nodes[0], nodes[1], color="red", marker="o", alpha=.5, s=5)

    plt.show()
    # """