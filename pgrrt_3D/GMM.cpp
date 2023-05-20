//
// Created by Paras Sharma on 6/7/2020.
//

#include <algorithm>
#include <random>
#include "GMM.h"
#include <chrono>

void GMM::normalize(){
    float total_var = 0.f;
    for (auto gauss: gauss_list){
        total_var += gauss.variance;
    }
    for (auto gauss: gauss_list){
        gauss.probability = 1 - gauss.variance/total_var;
    }
    std::sort(std::begin(gauss_list), std::end(gauss_list),
              [](Gaussian const & a, Gaussian const & b) -> bool
              { return a.variance < b.variance; } );
    float global_probability = 0.f;
    for (auto &gauss: gauss_list){
        gauss.probability_start = global_probability;
        gauss.probability_end = gauss.probability + gauss.probability_start;
        global_probability = gauss.probability_end;
    }
}

Gaussian GMM::find_nearest_gaussian(Gaussian gauss){
    sort(gauss_list.begin(), gauss_list.end(),
         [gauss](const Gaussian& a, const Gaussian& b)
         {
             return  std::min(std::fmod(std::abs(gauss.mean - a.mean), 360.), std::fmod(360 - std::abs(gauss.mean - a.mean),360)) < std::min(std::fmod(std::abs(gauss.mean - b.mean), 360.), std::fmod(360 - std::abs(gauss.mean - b.mean),360));
         });
    return gauss_list[0];
}

std::pair<float, Gaussian *> GMM::sample(){
    std::default_random_engine generator;
    //generator.seed(time(0));
    generator.seed();
    normalize();
    std::uniform_real_distribution<> dis(0, 1.0);
    float rand_ = dis(generator);
    auto iter =0;
    for(auto gauss: gauss_list){
        if(rand_ < gauss.probability_end){
            std::normal_distribution<double> distribution(gauss.mean, gauss.variance);
            return std::pair<float , Gaussian *>(distribution(generator), &gauss_list[iter]);
        }
        iter++;
    }
}

GMM::GMM() {

}

Gaussian::Gaussian(float mean_, float variance_, float probability_, float axis_) {
    mean = mean_;
    variance = variance_;
    probability = probability_;
    axis = axis_;
}
