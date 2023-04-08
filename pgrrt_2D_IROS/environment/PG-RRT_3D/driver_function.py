import math
import numpy as np


def eul_dist(point1, point2):
    """

    :param point1:
    :param point2:
    :return:
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def extend(node1, goal, growth):
    """

    :param node1:
    :param goal:
    :param growth:
    :return:
    """
    distance = eul_dist(node1, goal)
    ratio = growth/distance
    x3 = node1[0] + ratio*(goal[0] - node1[0])
    y3 = node1[1] + ratio*(goal[1] - node1[1])
    z3 = node1[2] + ratio*(goal[2] - node1[2])
    return (x3, y3, z3)

def rotate(origin, point, z, x):
    """

    :param origin:
    :param point:
    :param angle:
    :return:
    """
    z *= math.pi / 180
    x *= math.pi / 180
    ox, oy, oz = origin
    px, py, pz = point
    rot_z = np.asarray([[math.cos(z), -math.sin(z), 0.],
                        [math.sin(z), math.cos(z), 0.],
                        [          0.,            0., 1.]])
    rot_x = np.asarray([[1.,           0.,               0.],
                        [0., math.cos(x), -math.sin(x)],
                        [0., math.sin(x), math.cos(x)]])

    qx = px - ox
    qy = py - oy
    qz = pz - oz
    qx, qy, qz = np.dot(rot_x, np.dot(rot_z, np.transpose(np.asarray([qx, qy, qz]))))
    qx, qy, qz = qx+ox, qy+oy, qz+oz

    return qx, qy, qz


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


def sub_opt_path(path, tree):
    opt_path = [path[0]]
    node1 = path[0]
    node2 = path[-1]
    k = -1
    while node1 != path[-1] and k > -len(path):
        while node2 != node1:
            if not tree.canvas.check_collision(node1, node2,  tree.step_size*2**.5):
                opt_path.append(node2)
                node1 = node2
                node2 = path[-1]
            else:
                k -= 1
                node2 = path[k]
    cost = 0
    for node in range(1, len(opt_path)):
        cost += eul_dist(opt_path[node - 1], opt_path[node])
    return cost, opt_path


def get_path(tree, x):
    node = tree.nodes[x]
    path = []
    while node != tree.canvas.start:
        path.append(node)
        node = tree.parent[node]
    path.append(node)
    return path