class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, point, data):
        self.point = point
        self.data = data

class Quad:
    def __init__(self, topleft, botright, offset):
        self.n = None
        self.offset = offset
        self.topLeft = topleft
        self.botRight = botright
        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None

    def insert(self, node):
        if node is None:
            return

        if not self.inBoundary(node.point):
            return

        if abs(self.topLeft.x - self.botRight.x) <= self.offset and abs(self.topLeft.y - self.botRight.y) <= self.offset:
            if self.n is None:
                self.n = node
            return

        if (self.topLeft.x + self.botRight.x) / 2 >= node.point.x:
            if (self.topLeft.y + self.botRight.y) / 2 >= node.point.y:
                if self.topLeftTree is None:
                    self.topLeftTree = Quad(Point(self.topLeft.x, self.topLeft.y), Point((self.topLeft.x + self.botRight.x) / 2, (self.topLeft.y + self.botRight.y) / 2), self.offset)
                self.topLeftTree.insert(node)
            else:
                if self.botLeftTree is None:
                    self.botLeftTree = Quad(Point(self.topLeft.x, (self.topLeft.y + self.botRight.y) / 2), Point((self.topLeft.x + self.botRight.x / 2), self.botRight.y), self.offset)
                self.botLeftTree.insert(node)

        else:
            if (self.topLeft.y + self.botRight.y) / 2 >= node.point.y:
                if self.topRightTree is None:
                    self.topRightTree = Quad(Point((self.topLeft.x + self.botRight.x) / 2, self.topLeft.y), Point(self.botRight.x, (self.topLeft.y + self.botRight.y) / 2), self.offset)
                self.topRightTree.insert(node)
            else:
                if self.botRightTree is None:
                    self.botRightTree = Quad(Point((self.topLeft.x + self.botRight.x) / 2, (self.topLeft.y + self.botRight.y / 2)), Point(self.botRight.x, self.botRight.y), self.offset)
                self.botRightTree.insert(node)

    def search(self, point):
        if not self.inBoundary(point):
            return None

        if self.n is not None:
            return self.n

        if (self.topLeft.x + self.botRight.x) / 2 >= point.x:
            if (self.topLeft.y + self.botRight.y) / 2 >= point.y:
                if self.topLeftTree is None:
                    return None
                return self.topLeftTree.search(point)
            else:
                if self.botLeftTree is None:
                    return None
                return self.botLeftTree.search(point)
        else:
            if (self.topLeft.y + self.botRight.y) / 2 >= point.y:
                if self.topRightTree is None:
                    return None
                return self.topRightTree.search(point)
            else:
                if self.botRightTree is None:
                    return None
                return self.botRightTree.search(point)

    def inBoundary(self, point):
        return self.topLeft.x <= point.x <= self.botRight.x and self.topLeft.y <= point.y <= self.botRight.y

#
# center = Quad(Point(0, 0), Point(8, 8))
# a = Node(Point(1, 1), (1, 1))
# b = Node(Point(2, 5), (2, 5))
# c = Node(Point(7, 6), (7, 6))
# center.insert(a)
# center.insert(b)
# center.insert(c)
# print(center.search(Point(1,1)).data)
