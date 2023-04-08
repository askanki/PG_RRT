import copy
import datetime
import math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import random
from shapely.geometry import LineString, Point, Polygon

import tkinter  # matplotlib dependency

"""///////////////////////////////////"""
from map_canvas import Canvas
import point_cloud
from probability_dist import GMM, Gaussian

max_angle = 45
class Tree:
    def __init__(self, canvas, threshold_theta=90, resolution_angle=30, step_size=0.5):
        self.canvas = canvas
        self.threshold_theta = threshold_theta
        self.resolution_angle = resolution_angle
        self.step_size = step_size
        """////////////////////////////////////////"""
        self.nodes = []
        self.available_yaws = {}  # Dictionary node -> available_yaws
        self.rejected_yaws = {}
        self.actions = {}  # Dictionary node -> currently unexplored yaws
        self.parents = {}  # Dictionary node -> list of parents of node
        self.parent = {}
        self.prob_dist = {}
        self.special_nodes = []
        self.prev_special_nodes = []
        # self.used_special_nodes = {}
        """////////////////////////////////////////"""
        self.nodes.append(canvas.start)
        self.prob_dist[canvas.start] = GMM([Gaussian(5, 10, 0.5), Gaussian(-5 % 360, 10, 0.5)])
        self.parents[canvas.start] = set((canvas.start, 0))
        self.actions[canvas.start] = [0]
        self.available_yaws[canvas.start] = set([0])
        self.rejected_yaws[canvas.start] = set()
        self.special_nodes.append(canvas.start)
        self.parent[canvas.start] = canvas.start

    def add_node(self, parent, node, gauss, parent_yaw):
        collision_free = True
        if not self.canvas.adv_check_collision(node, parent, self.step_size):
            flag = 0
            for node_ in self.nodes:
                plot_flag = 0
                if eul_dist(node_, node) < 1.1*self.step_size / (2 ** .5) and node_ != node:
                    collision_free = False
                    flag = 1
                    for angle in range(0, 360, self.resolution_angle):
                        if feasible(parent, parent_yaw, node_, angle):
                            if angle not in self.rejected_yaws[node_]:
                                if angle not in self.available_yaws[node_]:
                                    self.available_yaws[node_].add(angle)
                                    if node_ not in self.actions:
                                        self.actions[node_] = []
                                    self.actions[node_].append(angle)
                                    if plot_flag==0:
                                        plt.plot([parent[0], node_[0]], [parent[1], node_[1]], color="red", alpha=0.2)
                                        plot_flag=1
                                    if (node_, angle) not in self.parents:
                                        self.parents[(node_, angle)] = set([])
                                    self.parents[(node_, angle)].add((parent, parent_yaw))
                                    if node_ not in self.special_nodes:
                                        self.special_nodes.append(node_)
            if flag == 0:
                self.nodes.append(node)
                # self.parents[node] = set([])
                self.available_yaws[node] = set([])
                self.rejected_yaws[node] = set([])
                self.actions[node] = []
                self.parent[node] = parent
                for angle in range(0, 360, self.resolution_angle):
                    if feasible(parent, parent_yaw, node, angle):
                        self.actions[node].append(angle)
                        if (node, angle) not in self.parents:
                            self.parents[(node, angle)] = set([])
                        self.parents[(node, angle)].add((parent, parent_yaw))

                self.prob_dist[node] = copy.deepcopy(self.prob_dist[parent])  # copy the gaussian of parent
                for gauss_ in self.prob_dist[node].gauss_list:  # modify gaussian of node with bias towards goal
                    mean_shift = self.resolution_angle * 0.9
                    variance_shift = 2
                    gauss_.mean = shift_toward(gauss_.mean, 0, mean_shift)
                    gauss_.variance -= variance_shift
                    gauss_.variance = max(5, gauss_.variance)

                self.special_nodes.append(node)
                self.remove_special(node, parent)
                plt.plot([parent[0], node[0]], [parent[1], node[1]], color="blue", alpha=0.2)

        else:
            collision_free = False

        self.change_probability(gauss, collision_free)

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

    def make_action(self, node, sampled_direction):  # add new node sample point here
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
            self.remove_action(node, closest[0])
            return closest[1], closest[0]
        return False, False

    def remove_action(self, node, action):
        actions = self.actions[node]
        if action in actions:
            self.actions[node].pop(self.actions[node].index(action))  # TODO: can be made better
        if len(actions) == 0:
            self.actions.pop(node)
            self.prev_special_nodes.append(self.special_nodes.pop(self.special_nodes.index(node)))


def feasible(node1, theta1, node2, theta2):
    if dist_mean(theta1, theta2) >= max_angle:
        return False
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


def pick_random(tree, iterations):
    while True:
        iterations+=1
        if len(tree.special_nodes) == 0:
            tree.special_nodes = set()
            for nodes in tree.prev_special_nodes:  # can be optimized
                nodes = tree.parent[nodes]
                if nodes != tree.canvas.start and (tree.canvas.start not in tree.actions):
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
        new_node, parent_yaw = tree.make_action(parent, sample_direction)
        if new_node and parent_yaw not in tree.rejected_yaws[parent]:
            tree.rejected_yaws[parent].add(parent_yaw)
            return parent, new_node, gauss, parent_yaw, iterations
        else:
            tree.prev_special_nodes.append(tree.special_nodes.pop(tree.special_nodes.index(parent)))


def termination(tree1, tree2, new_node):
    if eul_dist((tree2.canvas.start), new_node) < 0.5 * tree1.step_size:
        print(eul_dist((tree2.canvas.start), new_node))
        return True, tree2.canvas.start

    for x in range(len(tree2.nodes)):
        if eul_dist(new_node, tree2.nodes[x]) < 0.5 * tree1.step_size:
            print(eul_dist(new_node, tree2.nodes[x]), new_node, tree2.nodes[x])
            return True, tree2.nodes[x]
    return False, []


def get_path(tree, last_node):
    class Node:
        def __init__(self, node, parent):
            self.node = node
            self.childs = []
            self.parent = parent

    queue = []
    nodes = {}
    for angle in range(0, 360, tree.resolution_angle):
        if (last_node, angle) in tree.parents:
            queue.append((last_node, angle))
            nodes[(last_node, angle)] = Node((last_node, angle), (last_node, angle))
    # print(tree.available_yaws[last_node], tree.actions[last_node])
    visited = {}
    while True:
        current = queue.pop(0)
        if current[0] == tree.canvas.start:
            break
        if current in visited:
            continue
        visited[current] = True
        nodes[current].childs = tree.parents[current]
        for parent in nodes[current].childs:
            if parent not in visited:
                nodes[parent] = Node(parent, current)
                queue.append(parent)

    path = []
    while current[0]!=last_node:
        path.append(nodes[current].parent)
        next = nodes[current].parent
        plt.plot([current[0][0], next[0][0]], [current[0][1], next[0][1]], color="green")
        current = next
    # print(path)
    return path


def build_rrt():
    canvas = Canvas(Polygon([(0, -20), (40, -20), (40, 20), (0, 20)]), (1, 0), (13, -5))
    canvas1 = Canvas(Polygon([(0, -20), (40, -20), (40, 20), (0, 20)]), (13, -5), (1, 0))
    obstacles = point_cloud.get_obstacles()
    canvas.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    canvas1.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    tree = Tree(canvas)
    tree1 = Tree(canvas1)
    ######################################################
    obstacles = point_cloud.get_points()
    plt.figure(0)
    plt.axis("equal")
    for obs in obstacles:
        plt.scatter(obs[0], obs[1], marker="s", color="black", s=5)
    plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')
    plt.pause(0.01)
    iterations = 0
    while True:
        parent, new_node, gauss, parent_yaw, iterations = pick_random(tree, iterations)
        change = tree.add_node(parent, new_node, gauss, parent_yaw)
        parent1, new_node1, gauss1, parent_yaw1, iterations = pick_random(tree1, iterations)
        change1 = tree1.add_node(parent1, new_node1, gauss1, parent_yaw1)
        if change:
            terminate, end_node = termination(tree, tree1, new_node)
            if terminate:
                print("Terminated")
                plt.pause(2)
                get_path(tree, new_node)
                get_path(tree1, end_node)
                return tree, tree1, iterations
        if change1:
            terminate, end_node = termination(tree1, tree, new_node1)
            if terminate:
                print("Terminated")
                plt.pause(2)
                get_path(tree, end_node)
                get_path(tree1, new_node1)
                return tree1, tree, iterations
        # iterations += 2
        # if iterations % 500 == 0:
        #     plt.pause(0.01)
        #     print(iterations)


if __name__ == '__main__':
    print("Start time-stamp: ", datetime.datetime.now())
    tree, tree1, iterations = build_rrt()
    print("End time-stamp: ", datetime.datetime.now())
    print("Iterations: ", iterations)
    print("Nodes: ", len(tree.nodes) + len(tree1.nodes))
    # obstacles = point_cloud.get_points()
    # for obs in obstacles:
    #     plt.scatter(obs[0], obs[1], marker="s", color="black", s=5)
    # plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    # plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')

    # for nodes in tree.nodes:
    #     plt.scatter(nodes[0], nodes[1], color="blue", marker="o", alpha=.5, s=5)
    # for nodes in tree1.nodes:
    #     plt.scatter(nodes[0], nodes[1], color="red", marker="o", alpha=.5, s=5)

    plt.show()
