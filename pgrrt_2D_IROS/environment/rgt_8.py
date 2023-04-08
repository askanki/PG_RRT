import copy
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
from shapely.geometry import LineString, Point, Polygon

import tkinter  # matplotlib dependency

"""///////////////////////////////////"""
from map_canvas import Canvas
import point_cloud
from probability_dist import GMM, Gaussian
import cluster_map

global CHECK_SUM
CHECK_SUM = 0


class Tree:
    def __init__(self, canvas, threshold_theta=0, resolution_angle=15, step_size=0.5):
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
        # self.special_nodes = []  # List of special nodes
        # self.prev_special_nodes = []  # List of previous special nodes
        # self.used_special_nodes = {}  # Dictionary node -> bool, true if this nodes was a special node
        """////////////////////////"""
        self.canvas = canvas  # canvas contains start, end position and obstacles
        self.threshold_theta = threshold_theta  # parameter to sensitivity for special node
        self.resolution_angle = resolution_angle  # parameter to set resolution for actions
        self.step_size = step_size  # parameter to set step-size between two consecutive nodes
        """////////////////////////"""
        self.nodes.append(canvas.start)
        self.prob_dist[canvas.start] = GMM([Gaussian(0, 10, 0.5), Gaussian(-5 % 360, 10,
                                                                           0.5)])  # , Gaussian(25, 10, 0.1), Gaussian(-25 % 360, 10, 0.1), Gaussian(45, 10, 0.05), Gaussian(-45 % 360, 10, 0.05)])
        self.parent[canvas.start] = canvas.start
        # self.special_nodes.append(canvas.start)
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
        for angle in range(0, 360, resolution_angle):
            sample_location = rotate(node, sample, angle)
            flag = 0
            # CHECK_SUM += len(self.actions_taken)
            for node_ in self.actions_taken:  # Heavy operation, check if it can be replaced with quad-tree
                if eul_dist(node_, sample_location) < min(max(math.sqrt(2*(self.step_size**2) - 2*(self.step_size**2)*math.cos(resolution_angle*math.pi/180)) - 0.05, (self.step_size/2)*math.sqrt(2)), self.step_size - .1):
                    flag = 1
                    break
            if flag == 0:
                self.actions_taken[sample_location] = True
                action.append((angle, sample_location))
        if len(action) > 0:
            self.actions[node] = action
        # else:
        # plt.plot(node[0], node[1], color="red", marker="o")

    def add_node(self, parent, node, gauss):
        """

        :param parent: parent of the sampled node
        :param node: sampled node
        :param gauss: gaussian from which node was sampled
        :return: bool, True if successful, False otherwise
        """

        collision_free = True
        if not self.canvas.adv_check_collision(node, parent, self.step_size) and eul_dist(node, (20,0)) > 2:    # True if no obstacles
            self.nodes.append(node)
            self.parent[node] = parent
            self.setup_action(node, self.resolution_angle)
            # plt.plot([parent[0], node[0]], [parent[1], node[1]], color="blue")

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

            # self.special_nodes.append(node)
            # self.remove_special(node, parent)  # remove parent if not special

        return True if collision_free else False

    def change_probability(self, gauss, collision_free):
        """

        :param gauss: sampled gaussian
        :param collision_free:
        :return:
        """

        # if collision_free:
        #     mean_shift = self.resolution_angle * 0.9
        #     gauss.mean = shift_away(gauss.mean, 0, mean_shift)
        #     variance_shift = 2
        #     gauss.variance -= variance_shift
        #     gauss.variance = max(5, gauss.variance)
        #
        # else:
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
                if dist_mean(action[0], sampled_direction) < dist_mean(closest[0],
                                                                       sampled_direction):  # replace with dist function
                    closest = action
            self.remove_action(node, closest)
            return closest[1]
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
            # self.prev_special_nodes.append(self.special_nodes.pop(self.special_nodes.index(node)))
            # self.used_special_nodes[node] = True
            # plt.plot(node[0], node[1], color="red", marker="o")


def eul_dist(point1, point2):
    """

    :param point1:
    :param point2:
    :return:
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def extend(node1, goal, growth):
    """

    :param node1:
    :param goal:
    :param growth:
    :return:
    """
    distance = math.sqrt((node1[0] - goal[0]) ** 2 + (node1[1] - goal[1]) ** 2)
    ratio = growth / distance
    return ((1 - ratio) * node1[0] + ratio * goal[0]), ((1 - ratio) * node1[1] + ratio * goal[1])


def rotate(origin, point, angle):
    """

    :param origin:
    :param point:
    :param angle:
    :return:
    """
    angle *= math.pi / 180
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


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


def dist_mean(mean1, mean2):
    """

    :param mean1:
    :param mean2:
    :return:
    """
    return min(abs(mean1 - mean2) % 360, 360 - abs(mean1 - mean2) % 360)


def get_angle(a, b, c):
    """
    :param a:
    :param b:
    :param c:
    :return:
    """
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def path_cost(path, tree):
    def minDistance(dist, sptSet):
        min = math.inf
        min_index = -1
        for v in range(len(path)):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    def dijkstra(weigths, src):
        dist = [math.inf for i in range(len(path))]
        prev = [-1 for i in range(len(path))]
        dist[src] = 0
        sptSet = [False for i in range(len(path))]
        for cout in range(len(path)):
            u = minDistance(dist, sptSet)
            sptSet[u] = True
            for v in range(len(path)):
                if weigths[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + weigths[u][v]:
                    dist[v] = dist[u] + weigths[u][v]
                    prev[v] = u
        return dist[-1]

        # shortest_path = []
        # cur = len(path)-1
        # while cur != -1:
        #     shortest_path.append(cur)
        #     cur = prev[cur]
        # print(shortest_path)
        # for i in range(1, len(shortest_path)):
        #     plt.plot([path[shortest_path[i-1]][0], path[shortest_path[i]][0]], [path[shortest_path[i-1]][1], path[shortest_path[i]][1]], color="red")

    weigths = [[0 for x in range(len(path))] for i in range(len(path))]
    for node1 in range(len(path)):
        for node2 in range(len(path)):
            if not tree.canvas.check_collision(path[node1], path[node2]):  # True if obstacles
                weigths[node1][node2] = eul_dist(path[node1], path[node2])
            else:
                weigths[node1][node2] = math.inf
    return dijkstra(weigths, 0)


def sub_opt_path(path, tree):
    opt_path = [path[0]]
    node1 = path[0]
    node2 = path[-1]
    k = -1
    while node1 != path[-1] and k > -len(path):
        while node2 != node1:
            if not tree.canvas.check_collision(node1, node2):
                opt_path.append(node2)
                node1 = node2
                node2 = path[-1]
            else:
                k -= 1
                node2 = path[k]
    cost = 0
    for node in range(1, len(opt_path)):
        cost += eul_dist(opt_path[node - 1], opt_path[node])
    return cost


def get_path(tree, x):
    node = tree.nodes[x]
    path = []
    while node != tree.canvas.start:
        path.append(node)
        node = tree.parent[node]
    path.append(node)
    return path


def pick_random(tree):
    """

    :param tree:
    :return:
    """
    global CHECK_SUM
    while True:
        CHECK_SUM += 1
        # if len(tree.special_nodes) == 0:
        #     tree.special_nodes = set()
        #     for nodes in tree.prev_special_nodes:  # can be optimized
        #         while nodes in tree.used_special_nodes:
        #             nodes = tree.parent[nodes]
        #             if nodes == tree.canvas.start:
        #                 break
        #         if nodes != tree.canvas.start:
        #             tree.special_nodes.add(nodes)
        #     if len(tree.special_nodes) < 1:
        #         print("No path")
        #         # plt.pause(100)
        #         exit()
        #     tree.prev_special_nodes = []
        #     tree.special_nodes = list(tree.special_nodes)
        random_index = random.randint(0, len(tree.nodes) - 1)
        parent = tree.nodes[random_index]
        sample_direction, gauss = tree.prob_dist[parent].sample()
        new_node = tree.make_action(parent, sample_direction)
        if new_node:
            return parent, new_node, gauss
        # else:
        #     tree.prev_special_nodes.append(tree.special_nodes.pop(tree.special_nodes.index(parent)))
        #     tree.used_special_nodes[parent] = True


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


def build_rrt():
    """

    :return:
    """
    # plt.axis("equal")
    # canvas = Canvas(Polygon([(0, -20), (40, -20), (40, 20), (0, 20)]), (1, -5), (13, -5))
    # canvas1 = Canvas(Polygon([(0, -20), (40, -20), (40, 20), (0, 20)]), (13, -5), (1, -5))
    canvas = Canvas(Polygon([(0, -20), (40, -20), (40, 20), (0, 20)]), (5, 0), (35, 0))
    canvas1 = Canvas(Polygon([(0, -20), (40, -20), (40, 20), (0, 20)]), (35, 0), (5, 0))
    # canvas = Canvas(Polygon([(-20, -20), (20, -20), (20, 20), (-20, 20)]), (-7, 5), (13, -5))
    # canvas1 = Canvas(Polygon([(-20, -20), (20, -20), (20, 20), (-20, 20)]), (13, -5), (-7, 5))
    # canvas = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (10, 15), (35, 17))
    # canvas1 = Canvas(Polygon([(-20, -20), (40, -20), (40, 20), (-20, 20)]), (35, 17), (10, 15))
    # cluster_map.run_map()
    obstacles = point_cloud.get_obstacles()
    canvas.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    canvas1.add_obstacle_map(point_cloud.get_obs_map(), obstacles, point_cloud.get_points())
    tree = Tree(canvas)
    tree1 = Tree(canvas1)
    print(tree.resolution_angle)
    iterations = 0
    # for obs in tree.canvas.obstacles:
    #     plt.plot(*obs.exterior.xy)
    # plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    # plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')
    # plt.pause(0.1)
    while True:
        parent, new_node, gauss = pick_random(tree)
        parent1, new_node1, gauss1 = pick_random(tree1)
        change = tree.add_node(parent, new_node, gauss)
        change1 = tree1.add_node(parent1, new_node1, gauss1)
        if change:
            index = termination(tree, tree1, new_node)
            if index:
                path1 = get_path(tree, -1)
                path2 = get_path(tree1, index)
                path1.reverse()
                path1.extend(path2)
                return tree, tree1, iterations, path1
        if change1:
            index = termination(tree1, tree, new_node1)
            if index:
                path1 = get_path(tree, index)
                path2 = get_path(tree1, -1)
                path1.reverse()
                path1.extend(path2)
                return tree, tree1, iterations, path1
        iterations += 2
        if iterations % 1000 == 0:
            # plt.pause(2)
            print(iterations, datetime.datetime.now())
            sys.stdout.flush()

    return tree, tree1, iterations


if __name__ == "__main__":
    avg_iter = 0
    avg_node = 0
    min_iter = 100000
    max_iter = 0
    min_nodes = 100000
    max_nodes = 0
    avg_cost = 0
    timediff = 0
    min_time = 10000000000
    max_time = 0
    avg_sub = 0
    min_calls = 100000000000
    max_calls = 0
    last_calls = 0
    for test in range(10):
        print("WITHOUT")
        start = datetime.datetime.now()
        print("Start time-stamp: ", start)
        tree, tree1, iterations, path = build_rrt()
        end = datetime.datetime.now()
        print("End time-stamp: ", end)
        print("Iterations: ", iterations)
        print("Nodes: ", len(tree.nodes) + len(tree1.nodes))
        max_calls = max(max_calls, CHECK_SUM - last_calls)
        min_calls = min(min_calls, CHECK_SUM - last_calls)
        print(CHECK_SUM/(test+1))
        print("Min calls: ", min_calls)
        print("Max calls: ", max_calls)
        last_calls = CHECK_SUM - last_calls
        plt.clf()
        avg_iter += iterations
        avg_node += len(tree.nodes) + len(tree1.nodes)
        max_iter = max(max_iter, iterations)
        min_iter = min(min_iter, iterations)
        max_nodes = max(max_nodes, len(tree.nodes) + len(tree1.nodes))
        min_nodes = min(min_nodes, len(tree.nodes) + len(tree1.nodes))
        print("Min iter: ", min_iter)
        print("Max iter: ", max_iter)
        print("Min nodes: ", min_nodes)
        print("Max nodes: ", max_nodes)
        print("Avg iter: ", avg_iter / (test + 1), test)
        print("Avg nodes: ", avg_node / (test + 1), test)
        min_time = min(min_time, (end - start).total_seconds())
        max_time = max(max_time, (end - start).total_seconds())
        timediff += (end - start).total_seconds()
        print("Min time: ", min_time)
        print("Max time: ", max_time)
        print("Avg time diff: ", timediff / (test + 1))
        sub_cost = 0
        for q in range(1, len(path)):
            sub_cost+=eul_dist(path[q-1], path[q])
        avg_sub+= sub_cost
        print("Avg SubOpt cost: ", avg_sub/(test + 1))
        # for nodes in path:
        #     plt.scatter(nodes[0], nodes[1], color="black", marker="o", alpha=.5, s=5)
        avg_cost+= path_cost(path, tree)
        print("Avg cost: ", avg_cost / (test + 1), test)


    # """ Uncomment these to see plot
    obstacles = point_cloud.get_points()
    for obs in obstacles:
        plt.scatter(obs[0], obs[1], marker="s", color="black", s=5)
    plt.plot(tree.canvas.start[0], tree.canvas.start[1], marker="o")
    plt.plot(tree.canvas.end[0], tree.canvas.end[1], marker='x')

    # for nodes in tree.nodes:
    #     plt.scatter(nodes[0], nodes[1], color="blue", marker="o", alpha=.5, s=5)
    # for nodes in tree1.nodes:
    #     plt.scatter(nodes[0], nodes[1], color="red", marker="o", alpha=.5, s=5)

    plt.show()
    # """