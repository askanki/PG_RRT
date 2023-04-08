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

    def check_collision(self, point, parent, dist):
        for obstacle in self.obstacles:
            if self.eul_dist_3d(obstacle, point) < dist:
                return True
        return False

    def eul_dist_3d(self, point1, point2):
        return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)**.5

