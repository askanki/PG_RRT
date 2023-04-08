import copy
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


class Tree:
    def __init__(self, canvas, threshold_theta=90, resolution_angle=90, step_size=0.5):
        self.nodes = []  # List of nodes in the Tree
        self.prob_dist = {}  # Dictionary of nodes -> probability distribution or GMM Model
        self.parent = {}  # Dictionary node -> parent of node
        self.actions = {}  # Dictionary node -> action space
        self.actions_taken = {}  # Dictionary action -> bool, global dictionary of actions, value is True if action is reserved by some node
        self.actions_parent = {} # Dictionary (node, theta) -> parent
        self.special_nodes = []  # List of special nodes
        self.prev_special_nodes = []  # List of previous special nodes
        self.used_special_nodes = {}  # Dictionary node -> bool, true if this nodes was a special node
        """////////////////////////"""
        self.canvas = canvas  # canvas contains start, end position and obstacles
        self.threshold_theta = threshold_theta  # parameter to sensitivity for special node
        self.resolution_angle = resolution_angle  # parameter to set resolution for actions
        self.step_size = step_size  # parameter to set step-size between two consecutive nodes
        """////////////////////////"""
        self.nodes.append(canvas.start)
        self.prob_dist[canvas.start] = GMM([Gaussian(5, 10, 0.5), Gaussian(-5 % 360, 10, 0.5)])
        self.parent[canvas.start] = canvas.start
        self.special_nodes.append(canvas.start)
        self.actions[canvas.start] = [0]
        self.actions_parent[(canvas.start, 0)] = [canvas.start]
        """////////////////////////"""
        self.setup_action(canvas.start, self.resolution_angle)
        self.actions_taken[canvas.start] = True

    def setup_action(self, node, resolution_angle):
        action = []
        for angle in range(0, 360, resolution_angle):
            # add feasibility condition here
            for parent_yaw in self.actions[self.parent[node]]:  # check for current available yaws only and activate if action is not taken
                if feasible_path(angle, parent_yaw, node, self.parent[node]):
                    if (node, angle) not in self.actions_parent:
                        self.actions_parent[(node, angle)] = []
                    action.append(angle)
                    self.actions_parent[(node, angle)].append(self.actions_parent)
                    # sample = extend(node, self.canvas.end, self.step_size)
                    # sample_location = rotate(node, sample, angle)
                    # flag = 0
                    # for node_ in self.actions_taken:  # Heavy operation, check if it can be replaced with quad-tree
                    #     if eul_dist(node_, sample_location) < min(math.sqrt(
                    #             2 * (self.step_size ** 2) - 2 * (self.step_size ** 2) * math.cos(
                    #                     resolution_angle * math.pi / 180)) - 0.1, self.step_size - 0.05):
                    #         flag = 1
                    #         # for every theta
                    #         # check kino-dynamics and add parent to action_parent_list of node_
                    #         # add to available_actions
                    #         # for theta in range(0, 360, resolution_angle):
                    #         #     if feasible_path(angle, theta, node, node_):
                    #         #         self.actions_parent[(node_, theta)].append(node)
                    #
                    # if flag == 0:
                    #     self.actions_taken[sample_location] = True
                    #     action.append((angle, sample_location))
                    #     for theta in range(0, 360, resolution_angle):
                    #         if feasible_path(angle, theta, node, sample_location):
                    #             self.actions_parent[(sample_location, theta)] = [node]
                        # for every theta
                        # check kino-dynamics and add to action_parent_list of sample location
                        # add to available_actions

        if len(action) > 0:
            self.actions[node] = action

    def add_node(self, parent, node, gauss):
        collision_free = True
        if not self.canvas.adv_check_collision(node, parent, self.step_size):  # True if no obstacles
            # add check_collision with nodes
            # if collision add parent to the actions of the matched node else execute setup action
            flag = 0
            for nodes in self.actions_taken:
                if eul_dist(nodes, node) < min(math.sqrt(
                                2 * (self.step_size ** 2) - 2 * (self.step_size ** 2) * math.cos(
                                        self.resolution_angle * math.pi / 180)) - 0.1, self.step_size - 0.05):
                    flag = 1
                    collision_free = False
                    # add parent to thetas of close nodes
                    for parent_yaw in self.actions[parent]:
                        for theta in range(0, 360, self.resolution_angle):
                            if feasible_path(parent_yaw, theta, parent, nodes):
                                if theta not in self.actions[nodes]:
                                    self.actions[nodes].append(theta)
                                    self.actions_parent[(nodes, theta)] = []
                                self.actions_parent[(nodes, theta)].append(parent)

            if flag == 0:
                self.nodes.append(node)
                # self.actions[node] = []
                self.actions_taken[node] = True
                self.parent[node] = parent
                self.setup_action(node, self.resolution_angle)
                plt.plot([parent[0], node[0]], [parent[1], node[1]], color="blue")

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

            self.special_nodes.append(node)
            self.remove_special(node, parent)  # remove parent if not special

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

    def remove_special(self, node, parent):
        if self.parent[parent] != parent and self.check_threshold(node, parent):
            if parent in self.special_nodes:
                self.special_nodes.pop(self.special_nodes.index(parent))

    def check_threshold(self, node, parent):
        if min(get_angle(node, parent, self.parent[parent]),
               abs(360 - get_angle(node, parent, self.parent[parent]))) > 180 - self.threshold_theta:
            return True
        return False

    def make_action(self, node, sampled_direction): # add new node sample point here
        if node in self.actions:
            actions = self.actions[node]
            if len(actions) < 1:
                self.actions.pop(node)
                return False
            closest = actions[0]
            for action in actions:
                if dist_mean(action, sampled_direction) < dist_mean(closest,
                                                                       sampled_direction):  # replace with dist function
                    closest = action
            sample = extend(node, self.canvas.end, self.step_size)
            sample_location = rotate(node, sample, closest)
            closest = (closest, sample_location)
            self.remove_action(node, closest) # redefine
            return closest[1]
        return False

    def remove_action(self, node, action):
        actions = self.actions[node]
        if action in actions:
            self.actions[node].pop(self.actions[node].index(action))
        if len(actions) == 0:
            self.actions.pop(node)
            self.prev_special_nodes.append(self.special_nodes.pop(self.special_nodes.index(node)))
            self.used_special_nodes[node] = True


def feasible_path(theta1, theta2, node1, node2):
    return True


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


def pick_random(tree):
    while True:
        if len(tree.special_nodes) == 0:
            tree.special_nodes = set()
            for nodes in tree.prev_special_nodes:  # can be optimized
                while nodes in tree.used_special_nodes:
                    nodes = tree.parent[nodes]
                    if nodes == tree.canvas.start:
                        break
                if nodes != tree.canvas.start:
                    tree.special_nodes.add(nodes)
            if len(tree.special_nodes) < 1:
                print("No path")
                plt.pause(100)
                exit()
            tree.prev_special_nodes = []
            tree.special_nodes = list(tree.special_nodes)
        random_index = random.randint(0, len(tree.special_nodes) - 1)
        parent = tree.special_nodes[random_index]
        sample_direction, gauss = tree.prob_dist[parent].sample()
        new_node = tree.make_action(parent, sample_direction)
        if new_node:
            return parent, new_node, gauss
        else:
            tree.prev_special_nodes.append(tree.special_nodes.pop(tree.special_nodes.index(parent)))
            tree.used_special_nodes[parent] = True


def termination(tree1, tree2, new_node):
    if eul_dist((tree1.canvas.end), new_node) < 0.1:
        return True

    for x in range(len(tree2.nodes)):
        if eul_dist(new_node, tree2.nodes[x]) < 0.5 * tree1.step_size:
            return True
    return False


def build_rrt():
    canvas = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (1, 0), (13, -5))
    canvas1 = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (13, -5), (1, 0))
    obstacles = point_cloud.get_obstacles()
    canvas.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    canvas1.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    tree = Tree(canvas)
    tree1 = Tree(canvas1)
    ######################################################
    obstacles = point_cloud.get_points()
    for obs in obstacles:
        plt.scatter(obs[0], obs[1], marker="s", color="black", s=5)
    plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')
    plt.pause(0.01)
    ######################################################
    iterations = 0
    while True:
        parent, new_node, gauss = pick_random(tree)
        parent1, new_node1, gauss1 = pick_random(tree1)
        change = tree.add_node(parent, new_node, gauss)
        change1 = tree1.add_node(parent1, new_node1, gauss1)
        if change:
            if termination(tree, tree1, new_node):
                return tree, tree1, iterations
        if change1:
            if termination(tree1, tree, new_node1):
                return tree, tree1, iterations
        iterations += 2
        if iterations % 1 == 0:
            plt.pause(0.01)
        print(iterations)

    return tree, tree1, iterations, []


if __name__ == "__main__":
    print("Start time-stamp: ", datetime.datetime.now())
    tree, tree1, iterations = build_rrt()
    print("End time-stamp: ", datetime.datetime.now())
    print("Iterations: ", iterations)
    print("Nodes: ", len(tree.nodes) + len(tree1.nodes))

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