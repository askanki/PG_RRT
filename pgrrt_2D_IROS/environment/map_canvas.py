from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString
# import point_cloud


def leftmost_element(points, target_x):
    l = 0
    r = len(points)
    while l < r:
        m = (l + r)//2
        if points[m][0] < target_x:
            l = m + 1
        else:
            r = m
    return l


def rightmost_element(points, target_x):
    l = 0
    r = len(points)
    while l < r:
        m = (l + r)//2
        if points[m][0] > target_x:
            r = m
        else:
            l = m + 1
    return l - 1


class Canvas:
    def __init__(self, bounding_poly, start_point, end_point):
        self.obstacles = []
        self.obs_map = {}
        self.obs_points = []
        self.bounding_poly = bounding_poly
        self.start = start_point
        self.end = end_point

    def add_obstacle(self, polygon):
        self.obstacles.append(polygon)

    def add_obstacles(self, list):
        self.obstacles.extend(list)

    def add_obstacle_map(self, obs_map, obs, obs_points):
        self.obstacles = obs
        self.obs_map = obs_map
        self.obs_points = obs_points

    def check_collision(self, point, parent):
        line = LineString([point, parent])
        if not self.bounding_poly.intersects(line):
            return True
        for obstacle in self.obstacles:
            if obstacle.intersects(line):
                return True
        return False

    def adv_check_collision(self, point, parent, step_size):
        min_x = parent[0] - step_size*2
        max_x = parent[0] + step_size*2
        left_ind = leftmost_element(self.obs_points, min_x)
        right_ind = rightmost_element(self.obs_points, max_x)
        line = LineString([point, parent])
        if not self.bounding_poly.intersects(line):
            return True
        for obstacle in self.obs_points[left_ind: right_ind]:
            if self.obs_map[obstacle].intersects(line):
                return True
        return False

