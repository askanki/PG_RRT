//
// Created by Paras Sharma on 6/7/2020.
//

#ifndef PGRRT_GMM_H
#define PGRRT_GMM_H

#include <vector>

struct Gaussian{
    Gaussian(float mean_, float variance_, float probability_, float axis_);
    float mean;
    float variance;
    float probability;
    float axis;
    float probability_start{};
    float probability_end{};
};


class GMM {
public:
    GMM();
//    GMM(std::vector<Gaussian> &gaussList, bool extra) {
//        gauss_list = gaussList;
//    }

public:
    std::vector<Gaussian> gauss_list;
    void normalize();
    Gaussian find_nearest_gaussian(Gaussian gauss);

    std::pair<float, Gaussian> sample();
};



#endif //PGRRT_GMM_H
