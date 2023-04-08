import math
import numpy


def get_sheet(x, y, z, dist):
    samples=[]
    x_st = x[0]
    y_st = y[0]
    z_st = z[0]
    while z_st <= z[1]:
        while x_st <= x[1]:
            while y_st <= y[1]:
                samples.append([x_st, y_st, z_st])
                y_st += dist
            y_st = y[0]
            x_st += dist
        x_st = x[0]
        z_st += dist
    return samples



def get_gaussian_samples(mean, covariance, size):
    return numpy.random.multivariate_normal(mean, covariance, size)


def get_uniform_samples(x,y,z, size, dim=2):
    samples = []
    _min = [x[0], y[0], z[0]]
    _max = [x[1], y[1], z[1]]
    # print(_max, _min)
    return numpy.random.uniform(_min, _max, size=(size, dim))

def run_map():
    num_obs = 1000
    file = open("map1.txt", "w+")
    # samples = get_gaussian_samples([0,0], [[20,0], [0,20]], 0)
    # samples = get_uniform_samples([0, 20], [0, 20], [0, 20], 2000, dim=3)
    samples = get_sheet([5, 15], [5, 15], [5, 5], 0.2)
    samples.extend(get_sheet([5, 15], [5, 15], [7, 7], 0.2))
    samples.extend(get_sheet([5, 5], [5, 15], [5, 7], 0.2))
    samples.extend(get_sheet([15, 15], [5, 15], [5, 7], 0.2))
    samples.extend(get_sheet([5, 15], [5, 5], [5, 7], 0.2))
    samples.extend(get_sheet([5, 15], [15, 15], [5, 7], 0.2))
    print(len(samples))
    # print(samples)
    for sample in samples:
        file.write(str(sample[0]) + " " + str(sample[1]) + " " + str(sample[2]) + "\n")
    file.close()


run_map()