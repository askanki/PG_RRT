//
// Created by Paras Sharma on 6/7/2020.
//

#include <fstream>
#include <iostream>
#include <sstream>
#include <iterator>
#include <cmath>
#include "Canvas.h"
#include "Utils.h"

bool Canvas::check_collision(Node node1, Node node2, float step_size) {
    for(auto obs: obs_points){
        if(Utils::eul_dist(node1, obs) < step_size/pow(2, .5)){
            return true;
        }
    }
    return Utils::eul_dist(node1, node2) < step_size/pow(2, .5);
}

void Canvas::add_obstacles(std::vector<Node> obs) {
    obs_points = obs;
}

void Canvas::add_obs_from_file(std::string path_to_file) {
    std::string line;
    std::string word;
    std::ifstream obs_file (path_to_file);
    if (obs_file.is_open())
    {
        while (getline (obs_file,line))
        {
            std::vector<float> v;
            std::istringstream line_(line);
            std::copy(std::istream_iterator<float>(line_),
                      std::istream_iterator<float>(),
                      std::back_inserter(v));
            //obs_points.emplace_back(v[0], v[1], v[2]);
            obs_points.emplace_back(v[0], v[1], 0.);
        }
        obs_file.close();
    }

    else std::cout << "Unable to open file";
}
