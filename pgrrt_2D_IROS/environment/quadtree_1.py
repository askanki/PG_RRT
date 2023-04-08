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
        self.n = []
        self.topLeft = topleft
        self.botRight = botright
        self.offset = offset
        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None

    def insert(self, node):
        if node is None:
            return

        if not self.inBoundary(node.point):
            print(node.point.x, node.point.y, " - Not in Boundary")
            return

        if abs(self.topLeft.x - self.botRight.x) <= self.offset and abs(self.topLeft.y - self.botRight.y) <= self.offset:
            #print(node.point.x, node.point.y, "inserted in ", self.topLeft.x, self.topLeft.y, "  --  ", self.botRight.x, self.botRight.y)
            self.n.append(node)
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

    def search(self, point):
        if not self.inBoundary(point):
            return None

        if len(self.n) > 0:
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
        #print(self.topLeft.x, self.topLeft.y, "     ", self.botRight.x, self.botRight.y)
        return self.topLeft.x <= point.x <= self.botRight.x and self.topLeft.y <= point.y <= self.botRight.y


    def make_check(self, point, offset):
        offset = offset
        x1, y1 = point[0] - offset, point[1] + offset
        x3, y3 = point[0] + offset, point[1] - offset
        x2, y2 = point[0] + offset, point[1] + offset
        x4, y4 = point[0] - offset, point[1] - offset
        x5, y5 = point[0], point[1] + offset
        x6, y6 = point[0] + offset, point[1]
        x7, y7 = point[0], point[1] - offset
        x8, y8 = point[0] - offset, point[1]
        ans1 = self.search(Point(x1, y1))
        ans2 = self.search(Point(x2, y2))
        ans3 = self.search(Point(x3, y3))
        ans4 = self.search(Point(x4, y4))
        ans5 = self.search(Point(x5, y5))
        ans6 = self.search(Point(x6, y6))
        ans7 = self.search(Point(x7, y7))
        ans8 = self.search(Point(x8, y8))
        ans0 = self.search(Point(point[0], point[1]))
        answers = [ans0, ans1, ans2, ans3, ans4, ans5, ans6, ans7, ans8]
        #print(answers)
        for ans in answers:
            if ans is not None:
                return True
        return False

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
# x = center.search(Point(1.4,10.4))
# if x is not None:
#     for p in x:
#         print(p.data)
# else:
#     print(None)

# Store node in every chosen quad, log(n) storage per node, Searching and Inserting is still log(n), Memory is n*log(n)