//
// Created by Paras Sharma on 6/7/2020.
//

#include "GMM.h"

void GMM::normalize(){
    float total_var = 0.f;
    float total_prob = 0.f;
    
    //AG: Bug fix to update the probability of Gaussian
    for (auto &gauss: gauss_list){
        total_var += gauss.variance;
    }

    for (auto &gauss: gauss_list){
        gauss.probability = 1/gauss.variance; //(1 - gauss.variance/total_var);
        total_prob += gauss.probability;
    }

    for (auto &gauss: gauss_list){
        gauss.probability = gauss.probability/total_prob;
    }

    std::sort(std::begin(gauss_list), std::end(gauss_list),
              [](Gaussian const & a, Gaussian const & b) -> bool
              { return a.variance > b.variance; } );
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

std::pair<float, Gaussian *> GMM::sample(std::default_random_engine* generator){
    //std::default_random_engine generator;
    //generator.seed(time(0));
    //generator.seed(1686993888);
    //std::cout<<"Seed in GMM::sample is :"<<time(0)<<std::endl;
    normalize();
    std::uniform_real_distribution<> dis(0, 1.0);
    float rand_ = dis(*generator);
    //std::cout<<"rand_ value "<<rand_<<std::endl;
    auto iter =0;
    for(auto gauss: gauss_list){
        if(rand_ < gauss.probability_end){
            std::normal_distribution<double> distribution(gauss.mean, gauss.variance);
            float rand_norm_ = distribution(*generator);
            //std::cout<<"Rand norm value "<<rand_norm_<<std::endl;
            return std::pair<float , Gaussian *>(rand_norm_, &gauss_list[iter]);
        }
        iter++;
    }
}

GMM::GMM() {
    /*
    if(!is_updated){
        std::cout<<"Generator seed updated"<<std::endl;
        generator.seed(1686993888);
        is_updated = true;
    }*/
}

Gaussian::Gaussian(float mean_, float variance_, float probability_, float axis_) {
    mean = mean_;
    variance = variance_;
    probability = probability_;
    axis = axis_;
}
