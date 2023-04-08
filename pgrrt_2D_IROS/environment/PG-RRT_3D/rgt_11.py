import copy
import datetime
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import sys

import tkinter  # matplotlib dependency

"""///////////////////////////////////"""
from map_canvas_3d import Canvas
import point_cloud_3d
from probability_dist import GMM, Gaussian
import cluster_map
from driver_function import *

global CHECK_SUM
CHECK_SUM = 0
fig = plt.figure()
ax1 = fig.add_subplot(122, projection='3d')
PLOT = False
if PLOT: ax = fig.add_subplot(121, projection='3d')

class Tree:
    def __init__(self, canvas, threshold_theta=40, resolution_angle=45, step_size=0.5, n_long=2, color="blue"):
        """

        :param canvas: canvas contains start, end position and obstacles
        :param threshold_theta: parameter to sensitivity for special node
        :param resolution_angle: parameter to set resolution for actions
        :param step_size: parameter to set step-size between two consecutive nodes
        """

        self.nodes = []  # List of nodes in the Tree
        self.prob_dist = {}  # Dictionary of nodes -> probability distribution or GMM Model
        self.parent = {}  # Dictionary node -> parent of node
        self.actions = {}  # Dictionary node -> action space
        self.actions_taken = {}  # Dictionary action -> bool, global dictionary of actions, value is True if action is reserved by some node
        self.special_nodes = []  # List of special nodes
        self.prev_special_nodes = []  # List of previous special nodes
        self.used_special_nodes = {}  # Dictionary node -> bool, true if this nodes was a special node
        """////////////////////////"""
        self.canvas = canvas  # canvas contains start, end position and obstacles
        self.threshold_theta = threshold_theta  # parameter to sensitivity for special node
        self.resolution_angle = resolution_angle  # parameter to set resolution for actions
        self.step_size = step_size  # parameter to set step-size between two consecutive nodes
        self.n_long = n_long
        self.color = color
        """////////////////////////"""
        self.nodes.append(canvas.start)  # .225 .225 .125 .125 .075 .075 .05 .05 .025 .025
        self.prob_dist[canvas.start] = GMM([Gaussian(-5, 10, 0.5), Gaussian(5 % 360, 10, 0.5)])
        self.parent[canvas.start] = canvas.start
        self.special_nodes.append(canvas.start)
        """////////////////////////"""
        self.setup_action(canvas.start, self.resolution_angle)
        self.actions_taken[canvas.start] = True

    def setup_action(self, node, resolution_angle):
        """

        :param node: node
        :param resolution_angle: angle to divide the space
        :return:
        """

        # global CHECK_SUM
        action = []
        sample = extend(node, self.canvas.end, self.step_size)
        for longitude in range(0, 180, int(180//self.n_long)):
            for angle in range(0, 360, resolution_angle):
                sample_location = rotate(node, sample, angle, longitude)
                flag = 0
                if flag == 0:
                    self.actions_taken[sample_location] = True
                    action.append((longitude, angle, sample_location))
        if len(action) > 0:
            self.actions[node] = action


    def add_node(self, parent, node, gauss):
        """

        :param parent: parent of the sampled node
        :param node: sampled node
        :param gauss: gaussian from which node was sampled
        :return: bool, True if successful, False otherwise
        """

        collision_free = True
        for old_node in self.nodes:
            if eul_dist(old_node,
                        node) < self.step_size * 0.9:  # min(max(math.sqrt(2*(self.step_size**2) - 2*(self.step_size**2)*math.cos(self.resolution_angle*math.pi/180)) - 0.05, (self.step_size/2)*math.sqrt(2)), self.step_size - .08):
                collision_free = False

        if not self.canvas.check_collision(node, parent, self.step_size*2**.5) and collision_free:  # True if no obstacles
            self.nodes.append(node)
            self.parent[node] = parent
            self.setup_action(node, self.resolution_angle)
            if PLOT: ax.scatter([node[0]], [node[1]], [node[2]], color=self.color)

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
        """

        :param gauss: sampled gaussian
        :param collision_free:
        :return:
        """
        mean_shift = self.resolution_angle * 0.9
        gauss.mean = shift_away(gauss.mean, 0, mean_shift)
        variance_shift = 2
        gauss.variance += variance_shift
        gauss.variance = max(5, gauss.variance)

    def remove_special(self, node, parent):
        """

        :param node:
        :param parent:
        :return:
        """

        if self.parent[parent] != parent and self.check_threshold(node, parent):
            if parent in self.special_nodes:
                self.special_nodes.pop(self.special_nodes.index(parent))

    def check_threshold(self, node, parent):
        """

        :param node:
        :param parent:
        :return:
        """

        if min(get_angle(node, parent, self.parent[parent]),
               abs(360 - get_angle(node, parent, self.parent[parent]))) > 180 - self.threshold_theta:
            return True
        return False

    def make_action(self, node, sampled_direction):
        """

        :param node:
        :param sampled_direction:
        :return: bool, True if successful else False
        """

        if node in self.actions:
            actions = self.actions[node]
            if len(actions) < 1:
                self.actions.pop(node)
                return False
            closest = actions[0]
            for action in actions:
                if dist_mean(action[0], sampled_direction[0]) + dist_mean(action[1], sampled_direction[1]) < dist_mean(closest[0],
                                                                       sampled_direction[0]) + dist_mean(closest[1], sampled_direction[1]):  # replace with dist function
                    closest = action
            self.remove_action(node, closest)
            return closest[2]
        return False

    def remove_action(self, node, action):
        """

        :param node:
        :param action:
        :return:
        """

        actions = self.actions[node]
        if action in actions:
            self.actions[node].pop(self.actions[node].index(action))
        if len(actions) == 0:
            self.actions.pop(node)
            self.prev_special_nodes.append(self.special_nodes.pop(self.special_nodes.index(node)))
            self.used_special_nodes[node] = True


def shift_toward(mean, centre, shift):
    """

    :param mean:
    :param centre:
    :param shift:
    :return:
    """
    if abs(dist_mean((mean - shift), centre)) <= abs(dist_mean((mean + shift), centre)):
        mean -= shift
    else:
        mean += shift
    return mean % 360


def shift_away(mean, centre, shift):
    """

    :param mean:
    :param centre:
    :param shift:
    :return:
    """
    if abs(dist_mean((mean - shift), centre)) <= abs(dist_mean((mean + shift), centre)):
        mean += shift
    else:
        mean -= shift
    return mean % 360


def pick_random(tree):
    """

    :param tree:
    :return:
    """
    global CHECK_SUM
    while True:
        CHECK_SUM += 1
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
                # plt.pause(100)
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
    """

    :param tree1:
    :param tree2:
    :param new_node:
    :return:
    """
    if eul_dist((tree1.canvas.end), new_node) < 0.1:
        return True

    for x in range(len(tree2.nodes)):
        if eul_dist(new_node, tree2.nodes[
            x]) < 0.5 * tree1.step_size:  # and (not tree1.canvas.check_collision(new_node, tree2.nodes[x])):
            return x
    return False


def build_rrt(bounding_box, start_point, end_point):
    """

    :return:
    """
    canvas = Canvas(Bounding_box, start_point, end_point)
    canvas1 = Canvas(Bounding_box, end_point, start_point)
    obstacles = point_cloud_3d.get_obstacles()
    canvas.add_obstacle_map(point_cloud_3d.get_obs_map(), obstacles, point_cloud_3d.get_points())
    canvas1.add_obstacle_map(point_cloud_3d.get_obs_map(), obstacles, point_cloud_3d.get_points())
    tree = Tree(canvas, color="orange")
    tree1 = Tree(canvas1, color="yellow")
    print("Resolution  Angle: ", tree.resolution_angle)
    iterations = 0
    if PLOT:
        pointx = np.asarray([tree.canvas.start[0], tree.canvas.end[0]])
        pointy = np.asarray([tree.canvas.start[1], tree.canvas.end[1]])
        pointz = np.asarray([tree.canvas.start[2], tree.canvas.end[2]])
        ax.scatter(pointx, pointy, pointz, c='r', marker='o')

        x = obstacles[:,0]
        y = obstacles[:,1]
        z = obstacles[:,2]
        ax.scatter(x, y, z, c='black', marker='^')
        plt.pause(1)

    while True:
        parent, new_node, gauss = pick_random(tree)
        parent1, new_node1, gauss1 = pick_random(tree1)
        change = tree.add_node(parent, new_node, gauss)
        change1 = tree1.add_node(parent1, new_node1, gauss1)
        if change:
            index = termination(tree, tree1, new_node)
            if index:
                path1 = get_path(tree, -1); path2 = get_path(tree1, index)
                path1.reverse()
                path1.extend(path2)
                return tree, tree1, iterations, path1
        if change1:
            index = termination(tree1, tree, new_node1)
            if index:
                path1 = get_path(tree, index); path2 = get_path(tree1, -1)
                path1.reverse()
                path1.extend(path2)
                return tree, tree1, iterations, path1
        iterations += 2
        if iterations % 1000 == 0:
            if PLOT: plt.pause(2)
            print(iterations, datetime.datetime.now())
            sys.stdout.flush()

    return tree, tree1, iterations


if __name__ == "__main__":
    avg_iter = 0; avg_node = 0;
    min_iter = 100000; max_iter = 0
    min_nodes = 100000; max_nodes = 0
    avg_cost = 0
    timediff = 0; min_time = 10000000000; max_time = 0
    avg_sub = 0
    min_calls = 100000000000; max_calls = 0; last_calls = 0

    Bounding_box = [(0, -20, 0), (40, -20, 0), (40, 20, 0), (0, 20, 0)]
    start_point = (0, 10, 6)
    end_point = (20, 10, 6)
    for test in range(1):
        print("WITH")
        start = datetime.datetime.now()
        print("Start time-stamp: ", start)
        tree, tree1, iterations, path = build_rrt(Bounding_box, start_point, end_point)
        end = datetime.datetime.now()
        print("End time-stamp: ", end)
        sys.stdout.flush()
        print("Iterations: ", iterations); print("Nodes: ", len(tree.nodes) + len(tree1.nodes))
        max_calls = max(max_calls, CHECK_SUM - last_calls); min_calls = min(min_calls, CHECK_SUM - last_calls); last_calls = CHECK_SUM - last_calls
        print(CHECK_SUM / (test + 1))
        print("Min calls: ", min_calls)
        print("Max calls: ", max_calls)
        avg_iter += iterations; max_iter = max(max_iter, iterations); min_iter = min(min_iter, iterations)
        avg_node += len(tree.nodes) + len(tree1.nodes); max_nodes = max(max_nodes, len(tree.nodes) + len(tree1.nodes)); min_nodes = min(min_nodes, len(tree.nodes) + len(tree1.nodes))
        print("Min iter: ", min_iter); print("Max iter: ", max_iter); print("Min nodes: ", min_nodes); print("Max nodes: ", max_nodes); print("Avg iter: ", avg_iter / (test + 1), test); print("Avg nodes: ", avg_node / (test + 1), test)
        min_time = min(min_time, (end - start).total_seconds()); max_time = max(max_time, (end - start).total_seconds())
        timediff += (end - start).total_seconds()
        print("Min time: ", min_time)
        print("Max time: ", max_time)
        print("Avg time diff: ", timediff / (test + 1))
        leaf_cost = 0
        for q in range(1, len(path)):
            leaf_cost += eul_dist(path[q - 1], path[q])
            ax1.plot([path[q-1][0], path[q][0]], [path[q-1][1], path[q][1]], [path[q-1][2], path[q][2]], marker='o', color='green')
        avg_sub += leaf_cost
        print("Avg SubOpt cost: ", avg_sub / (test + 1))


    # """ Uncomment these to see plot
    if not PLOT:
        print("PLOTTING")
        ax = fig.add_subplot(121, projection='3d')
        obstacles = point_cloud_3d.get_obstacles()
        x = obstacles[:,0]
        y = obstacles[:,1]
        z = obstacles[:,2]
        ax.scatter(x, y, z, c='black', marker='^')
        ax1.scatter(x, y, z, c='black', marker='^')

        pointx = np.asarray([tree.canvas.start[0], tree.canvas.end[0]])
        pointy = np.asarray([tree.canvas.start[1], tree.canvas.end[1]])
        pointz = np.asarray([tree.canvas.start[2], tree.canvas.end[2]])
        ax.scatter(pointx, pointy, pointz, c='r', marker='o')
        ax1.scatter(pointx, pointy, pointz, c='r', marker='o')

        for q in range(1, len(path)):
            ax1.plot([path[q-1][0], path[q][0]], [path[q-1][1], path[q][1]], [path[q-1][2], path[q][2]], marker='o', color='green')

        for nodes in tree.nodes:
            ax.scatter(nodes[0], nodes[1], nodes[2], color="orange", marker="o")
        for nodes in tree1.nodes:
            ax.scatter(nodes[0], nodes[1], nodes[2], color="yellow", marker="o")

    plt.show()
    # """