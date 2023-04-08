import math
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, point, data):
        self.point = point
        self.data = data

class Quad:
    def __init__(self, topleft, botright, offset=1):
        self.n = set()
        self.topLeft = topleft
        self.botRight = botright
        self.offset = offset
        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None
        self.nodes = set()

    def insert(self, node):
        if node is None:
            return

        if not self.inBoundary(node.point):
            print(node.point.x, node.point.y, " - Not in Boundary")
            return

        self.nodes.add(node.point)

        if abs(self.topLeft.x - self.botRight.x) <= self.offset and abs(self.topLeft.y - self.botRight.y) <= self.offset:
            self.n.add(node)
            return

        if (self.topLeft.x + self.botRight.x) / 2 >= node.point.x:
            if (self.topLeft.y + self.botRight.y) / 2 >= node.point.y:
                if self.topLeftTree is None:
                    self.topLeftTree = Quad(Point(self.topLeft.x, self.topLeft.y), Point((self.topLeft.x + self.botRight.x) / 2, (self.topLeft.y + self.botRight.y) / 2), self.offset)
                self.topLeftTree.insert(node)
            else:
                if self.botLeftTree is None:
                    self.botLeftTree = Quad(Point(self.topLeft.x, (self.topLeft.y + self.botRight.y) / 2), Point((self.topLeft.x + self.botRight.x) / 2, self.botRight.y), self.offset)
                self.botLeftTree.insert(node)

        else:
            if (self.topLeft.y + self.botRight.y) / 2 >= node.point.y:
                if self.topRightTree is None:
                    self.topRightTree = Quad(Point((self.topLeft.x + self.botRight.x) / 2, self.topLeft.y), Point(self.botRight.x, (self.topLeft.y + self.botRight.y) / 2), self.offset)
                self.topRightTree.insert(node)
            else:
                if self.botRightTree is None:
                    self.botRightTree = Quad(Point((self.topLeft.x + self.botRight.x) / 2, (self.topLeft.y + self.botRight.y) / 2), Point(self.botRight.x, self.botRight.y), self.offset)
                self.botRightTree.insert(node)

    def search(self, point, offset, parent_node_list):
        if not self.inBoundary(point):
            return None
        if check_edge_dist(point, self.topLeft, self.botRight, 0.2):
            if len(parent_node_list) > 0:
                for node in parent_node_list:
                    if eul_dist(node, point) <= offset:
                        return True
            return False

        if len(self.n) > 0:
            for node in self.n:
                if eul_dist(node, point) <= offset:
                    return True
            return False

        if (self.topLeft.x + self.botRight.x) / 2 >= point.x:
            if (self.topLeft.y + self.botRight.y) / 2 >= point.y:
                if self.topLeftTree is None:
                    return False
                return self.topLeftTree.search(point, offset, self.nodes)
            else:
                if self.botLeftTree is None:
                    return False
                return self.botLeftTree.search(point, offset, self.nodes)
        else:
            if (self.topLeft.y + self.botRight.y) / 2 >= point.y:
                if self.topRightTree is None:
                    return False
                return self.topRightTree.search(point, offset, self.nodes)
            else:
                if self.botRightTree is None:
                    return False
                return self.botRightTree.search(point, offset, self.nodes)

    def inBoundary(self, point):
        return self.topLeft.x <= point.x <= self.botRight.x and self.topLeft.y <= point.y <= self.botRight.y


def eul_dist(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def check_edge_dist(point1, topleft, botright, offset):
    flag = 0
    if abs(point1.x - topleft.x) <= offset:
        flag = 1
    elif abs(point1.x - botright.x) <= offset:
        flag = 1
    elif abs(point1.y - topleft.y) <= offset:
        flag = 1
    elif abs(point1.y - botright.y) <= offset:
        flag = 1
    return True if flag==1 else False  # returns True if Distance is less.


# center = Quad(Point(0, 0), Point(50, 50))
# a = Node(Point(1.5, 10.5), 1)
# d = Node(Point(1.2, 1.3), 2)
# e = Node(Point(1.3, 1.4), 5)
# b = Node(Point(2, 5), 3)
# c = Node(Point(7, 6), 4)
# center.insert(a)
# center.insert(d)
# center.insert(b)
# center.insert(c)
# center.insert(e)
# x = center.search(Point(1.4,1.4), 0.5)
# if x is not None:
#     for p in x:
#         print(p.data)
# else:
#     print(None)

# Store node in every chosen quad, log(n) storage per node, Searching and Inserting is still log(n), Memory is n*log(n)