import random
import numpy as np
import copy

class GMM:
    def __init__(self, gauss_list, num_axis=1):
        self.num_axis = num_axis
        self.gauss_list = []
        for longitude in range(0, 180, int(180//self.num_axis)):
            for w in range(len(gauss_list)):
                gauss_ = copy.deepcopy(gauss_list[w])
                gauss_.longitude = longitude
                self.gauss_list.append(gauss_)

    def normalize(self):
        total = 0
        for gauss in self.gauss_list:
            total+=gauss.variance

        for gauss in self.gauss_list:
            gauss.prob = 1 - gauss.variance/total

        self.gauss_list.sort(key=lambda x: x.prob)

        global_prob = 0
        for gauss in self.gauss_list:
            gauss.prob_start = global_prob
            gauss.prob_end = gauss.prob + global_prob
            global_prob = gauss.prob_end

    def find_nearest_gaussian(self, gauss):
        self.gauss_list.sort(key= lambda x: min(abs(gauss.mean - x.mean)%360, (360 - abs(gauss.mean - x.mean)%360)))
        #print(self.gauss_list)
        return self.gauss_list[1]

    def sample(self):
        self.normalize()
        rand_ = random.uniform(0, 1)
        gauss = self.gauss_list[0]
        for gauss in self.gauss_list:
            if rand_ < gauss.prob_end:
                return (np.random.normal(gauss.mean, gauss.variance, 1)[0], gauss.longitude), gauss
        return (np.random.normal(gauss.mean, gauss.variance, 1)[0], gauss.longitude), gauss

class Gaussian:
     def __init__(self, mean, variance, prob):
         self.mean = mean
         self.variance = variance
         self.prob = prob
         self.prob_start = 0
         self.prob_end = prob
         self.longitude = 0.
     # def variance_to_probability(self):
     #     self.prob = 1/(1+self.variance)



