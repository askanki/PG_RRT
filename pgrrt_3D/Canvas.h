//
// Created by Paras Sharma on 6/7/2020.
//

#ifndef PGRRT_CANVAS_H
#define PGRRT_CANVAS_H

#include <tuple>
#include <vector>
#include <string>
#include "Utils.h"
#include "config.h"
#include <octomap/octomap.h>
#include <octomap/OcTree.h>
#include <dynamicEDT3D/dynamicEDTOctomap.h>

using namespace octomap;
using namespace octomath;

class Canvas {

public:
    //TODO: This can be extended to include the Axis information
    //start/end format - coordinate, yaw
    std::pair<Node, float> start;
    std::pair<Node, float> end;
    std::vector <Node> obs_points;
    OcTree *obsmap;
    DynamicEDTOctomap *obsdistmap;
    
    double min_x, max_x, min_y, max_y, min_z, max_z;
    void add_obstacles(std::vector <Node> obs);
    void add_obs_from_file(std::string path_to_file);
    void add_obs_from_octomap(std::string path_to_file);
    bool check_collision(Node node1, Node node2, float step_size);
};


#endif //PGRRT_CANVAS_H
